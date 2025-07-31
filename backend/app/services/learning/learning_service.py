import asyncio
import json
import hashlib
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, asdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import PydanticOutputParser

from app.models import (
    Topic,
    Card,
    LearningSession
)
from app.schemas.learning import QACard, QABatch, GenerationMode
from app.config import redis_client, settings
from .prompts import topic_analysis_prompt, qa_generation_prompt


@dataclass(frozen=True)
class TopicAnalysis:
    """Topic analysis data"""
    concepts: list[str]
    hooks: list[str]
    misconceptions: list[str]
    prerequisites: list[str]
    difficulty_range: dict[str, int]


@dataclass(frozen=True)
class LearningSessionData:
    """Learning session data"""
    topic: Topic
    session: LearningSession
    topic_analysis: TopicAnalysis
    buffer: list[Card]
    current_index: int
    generation_task: Optional[asyncio.Task]


class LearningService:
    """Core service for managing learning sessions and content generation"""

    def __init__(self, db: AsyncSession):
        self.db = db

        self.primary_llm = ChatOpenAI(
            model=settings.DEFAULT_LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY
        )

        if settings.ANTHROPIC_API_KEY:
            self.fallback_llm = ChatAnthropic(
                model="claude-3-haiku-20240307",
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                anthropic_api_key=settings.ANTHROPIC_API_KEY
            )
        else:
            self.fallback_llm = None
        self.qa_parser = PydanticOutputParser(pydantic_object=QABatch)
        self.active_sessions: dict[str, dict] = {}

    async def initialize_session(
        self,
        topic_id: str,
        user_id: str,
        mode: GenerationMode = GenerationMode.STANDARD
    ) -> Dict:
        """Initialize a new learning session"""
        result = await self.db.execute(
            select(Topic).where(Topic.id == topic_id)
        )
        topic = result.scalar_one()

        if not topic.topic_structure:
            topic_analysis = await self._analyze_topic(topic.name)
            topic.topic_structure = asdict(topic_analysis)
            topic.core_concepts = topic_analysis.concepts
            await self.db.commit()
        else:
            topic_analysis = TopicAnalysis(**topic.topic_structure)

        session = LearningSession(
            user_id=user_id,
            topic_id=topic_id,
            session_type=mode.value,
            card_queue=[],
            asked_questions=[],
            covered_concepts=[]
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)

        initial_cards = await self._generate_initial_batch(
            topic=topic,
            session=session,
            topic_analysis=topic_analysis
        )

        self.active_sessions[session.id] = {
            "topic": topic,
            "session": session,
            "topic_analysis": topic_analysis,
            "buffer": initial_cards,
            "current_index": 0,
            "generation_task": None
        }

        asyncio.create_task(self._maintain_buffer(session.id))

        return {
            "session_id": session.id,
            "initial_cards": [self._card_to_dict(card) for card in initial_cards[:5]],
            "total_concepts": len(topic_analysis.concepts)
        }

    async def get_next_card(self, session_id: str) -> Optional[Dict]:
        """Get next card from session buffer"""
        session_data = self.active_sessions.get(session_id)
        if not session_data:
            session_data = await self._load_session(session_id)
            if not session_data:
                return None

        buffer = session_data["buffer"]
        current_index = session_data["current_index"]

        if current_index < len(buffer):
            card = buffer[current_index]
            session_data["current_index"] += 1

            # Update session progress in DB
            session = session_data["session"]
            session.current_card_index = current_index + 1
            session.cards_viewed += 1
            await self.db.commit()

            # Trigger generation if buffer is low
            if len(buffer) - current_index < 5:
                asyncio.create_task(self._generate_more_cards(session_id))

            return self._card_to_dict(card)

        return None

    async def _analyze_topic(self, topic_name: str) -> TopicAnalysis:
        """Analyze topic structure using LLM"""
        cache_key = f"topic_analysis:{hashlib.md5(topic_name.encode()).hexdigest()}"
        cached = await redis_client.get(cache_key)
        if cached:
            return TopicAnalysis(**json.loads(cached))

        messages = topic_analysis_prompt.format_messages(topic=topic_name)

        try:
            response = await self.primary_llm.ainvoke(messages)
            analysis = json.loads(response.content)
        except Exception as e:
            if self.fallback_llm:
                response = await self.fallback_llm.ainvoke(messages)
                analysis = json.loads(response.content)
            else:
                analysis = TopicAnalysis(
                    concepts=[f"{topic_name} Basics",
                              f"Advanced {topic_name}"],
                    hooks=["Interactive learning"],
                    misconceptions=[],
                    prerequisites=[],
                    difficulty_range={"min": 1, "max": 5}
                )

        await redis_client.setex(cache_key, 604800, json.dumps(asdict(analysis)))
        return analysis

    async def _generate_initial_batch(
        self,
        topic: Topic,
        session: LearningSession,
        topic_analysis: TopicAnalysis
    ) -> list[Card]:
        """Generate initial batch of cards"""
        result = await self.db.execute(
            select(Card)
            .where(Card.topic_id == topic.id)
            .order_by(Card.difficulty)
            .limit(20)
        )
        existing_cards = result.scalars().all()

        if len(existing_cards) >= 5:
            return existing_cards[:5]

        concepts_to_cover = topic_analysis.concepts[:5]
        qa_batch = await self._generate_qa_batch(
            topic_name=topic.name,
            concepts=concepts_to_cover,
            count=10,
            previous_questions=set()
        )

        # Save cards to database
        cards = []
        for qa_card in qa_batch.cards:
            card = Card(
                topic_id=topic.id,
                question=qa_card.question,
                answer=qa_card.answer,
                difficulty=qa_card.difficulty,
                concept_tag=qa_card.concept_tag,
                generation_model=settings.DEFAULT_LLM_MODEL
            )
            self.db.add(card)
            cards.append(card)

        await self.db.commit()

        session.card_queue = [card.id for card in cards]
        session.asked_questions = [card.question for card in cards]
        session.covered_concepts = concepts_to_cover
        await self.db.commit()

        return cards

    async def _generate_qa_batch(
        self,
        topic_name: str,
        concepts: List[str],
        count: int,
        previous_questions: Set[str]
    ) -> QABatch:
        """Generate batch of Q&A cards using LLM"""
        prev_q_formatted = "\n".join(
            previous_questions) if previous_questions else "None"

        messages = qa_generation_prompt.format_messages(
            topic=topic_name,
            concepts=", ".join(concepts),
            previous_questions=prev_q_formatted,
            count=count,
            format_instructions=self.qa_parser.get_format_instructions()
        )

        try:
            response = await self.primary_llm.ainvoke(messages)
            qa_batch = self.qa_parser.parse(response.content)
        except Exception:
            qa_batch = QABatch(
                cards=[
                    QACard(
                        question=f"What is {concepts[0]}?",
                        answer=f"**{concepts[0]}** is a key concept in {topic_name}",
                        difficulty=2,
                        concept_tag=concepts[0]
                    )
                    for i in range(min(count, len(concepts)))
                ],
                topic=topic_name,
                session_context=f"Emergency generation for {topic_name}"
            )

        return qa_batch

    async def _maintain_buffer(self, session_id: str):
        """Background task to maintain card buffer"""
        while session_id in self.active_sessions:
            session_data = self.active_sessions[session_id]
            buffer = session_data["buffer"]
            current_index = session_data["current_index"]

            # Calculate remaining cards
            remaining = len(buffer) - current_index

            if remaining < 10:
                # Generate more cards
                await self._generate_more_cards(session_id)

            # Check every 5 seconds
            await asyncio.sleep(5)

    async def _generate_more_cards(self, session_id: str):
        """Generate additional cards for session"""
        session_data = self.active_sessions.get(session_id)
        if not session_data:
            return

        topic = session_data["topic"]
        session = session_data["session"]
        topic_analysis = session_data["topic_analysis"]

        all_concepts = topic_analysis["concepts"]
        covered = set(session.covered_concepts)
        remaining = [c for c in all_concepts if c not in covered]

        if not remaining:
            next_concepts = all_concepts[:3]
        else:
            next_concepts = remaining[:3]

        qa_batch = await self._generate_qa_batch(
            topic_name=topic.name,
            concepts=next_concepts,
            count=5,
            previous_questions=set(session.asked_questions)
        )

        new_cards = []
        for qa_card in qa_batch.cards:
            card = Card(
                topic_id=topic.id,
                question=qa_card.question,
                answer=qa_card.answer,
                difficulty=qa_card.difficulty,
                concept_tag=qa_card.concept_tag,
                generation_model=settings.DEFAULT_LLM_MODEL
            )
            self.db.add(card)
            new_cards.append(card)

        await self.db.commit()

        # Update session
        session_data["buffer"].extend(new_cards)
        session.card_queue.extend([card.id for card in new_cards])
        session.asked_questions.extend([card.question for card in new_cards])
        session.covered_concepts.extend(next_concepts)

        await self.db.commit()

    async def _load_session(self, session_id: str) -> Optional[Dict]:
        """Load session from database"""
        result = await self.db.execute(
            select(LearningSession)
            .options(selectinload(LearningSession.topic))
            .where(LearningSession.id == session_id)
        )
        session = result.scalar_one_or_none()

        if not session:
            return None

        card_ids = session.card_queue[session.current_card_index:]
        result = await self.db.execute(
            select(Card).where(Card.id.in_(card_ids))
        )
        cards = result.scalars().all()

        # Restore session to memory
        session_data = {
            "topic": session.topic,
            "session": session,
            "topic_analysis": session.topic.topic_structure,
            "buffer": cards,
            "current_index": 0,
            "generation_task": None
        }

        self.active_sessions[session_id] = session_data

        # Restart buffer maintenance
        asyncio.create_task(self._maintain_buffer(session_id))

        return session_data

    def _card_to_dict(self, card: Card) -> Dict:
        """Convert card model to dictionary"""
        return {
            "id": card.id,
            "question": card.question,
            "answer": card.answer,
            "difficulty": card.difficulty,
            "concept_tag": card.concept_tag
        }
