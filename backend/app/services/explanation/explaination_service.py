import asyncio
import json
import hashlib
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
import redis.asyncio as redis

from app.models import Card, User, CardInteraction, Topic
from app.config.settings import settings
from app.config import redis_client


class ExplanationService:
    """Service for generating and refining card explanations"""

    def __init__(self, db: AsyncSession):
        self.db = db

        self.explanation_llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.3,
            max_tokens=800,
            openai_api_key=settings.OPENAI_API_KEY
        )

        # Prompts
        self._init_prompts()

        # Cache TTL
        self.explanation_cache_ttl = 3600 * 24  # 24 hours

    def _init_prompts(self):
        """Initialize explanation prompts"""
        self.explanation_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert educator providing clear, engaging explanations.
            
            Your explanations should:
            1. Start with the core concept in simple terms
            2. Build up complexity gradually
            3. Use analogies and real-world examples
            4. Include a practical code example or application
            5. End with a "pro tip" or common pitfall to avoid
            
            Format your response in markdown with clear sections.
            Keep it concise but comprehensive (300-500 words).
            Make it feel like a friendly expert is teaching them."""),

            HumanMessage(content="""
            Card Question: {question}
            Card Answer: {answer}
            Topic: {topic}
            Concept: {concept}
            User Level: {user_level}
            
            Provide a detailed explanation that helps the user deeply understand this concept.
            
            Structure:
            ## 📚 Core Concept
            [Simple explanation]
            
            ## 🔍 Deep Dive
            [Detailed explanation with why/how]
            
            ## 💡 Real-World Analogy
            [Relatable comparison]
            
            ## 💻 Practical Example
            ```language
            [Code example]
            ```
            
            ## ⚡ Pro Tip
            [Advanced insight or common mistake to avoid]
            """)
        ])

        self.refinement_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are refining an explanation based on user feedback.
            
            Key principles:
            1. Address the specific concern or question
            2. Don't repeat the entire explanation
            3. Add new information or clarify confusion
            4. Keep the same friendly, expert tone
            5. If asked for more examples, provide different ones
            6. If asked to simplify, use more basic language
            7. If asked for more depth, add technical details"""),

            HumanMessage(content="""
            Original Question: {question}
            Original Answer: {answer}
            
            Current Explanation:
            {current_explanation}
            
            User Request: {refinement_request}
            
            Provide a refined explanation that addresses their specific request.
            Keep the same markdown structure but update the relevant sections.
            """)
        ])

    async def generate_explanation(
        self,
        card_id: str,
        user_id: str,
        session_id: Optional[str] = None
    ) -> Dict:
        """Generate detailed explanation for a card"""
        # Get card details
        result = await self.db.execute(
            select(Card).where(Card.id == card_id)
        )
        card = result.scalar_one_or_none()

        if not card:
            raise ValueError("Card not found")

        # Check cache first
        cache_key = f"explanation:{card_id}:{user_id}"
        cached = await redis_client.get(cache_key)

        if cached:
            return json.loads(cached)

        # Get user details for personalization
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one()

        # Get topic details
        result = await self.db.execute(
            select(Topic).where(Topic.id == card.topic_id)
        )
        topic = result.scalar_one()

        # Generate explanation
        messages = self.explanation_prompt.format_messages(
            question=card.question,
            answer=card.answer,
            topic=topic.name,
            concept=card.concept_tag,
            user_level=self._get_user_level(user.preferred_difficulty)
        )

        response = await self.explanation_llm.ainvoke(messages)
        explanation_text = response.content

        # Create explanation object
        explanation = {
            "id": hashlib.md5(f"{card_id}:{user_id}:{datetime.utcnow().isoformat()}".encode()).hexdigest(),
            "card_id": card_id,
            "explanation": explanation_text,
            "generated_at": datetime.utcnow().isoformat(),
            "refinement_count": 0,
            "user_level": user.preferred_difficulty,
            "metadata": {
                "topic": topic.name,
                "concept": card.concept_tag,
                "difficulty": card.difficulty
            }
        }

        # Cache the explanation
        await redis_client.setex(
            cache_key,
            self.explanation_cache_ttl,
            json.dumps(explanation)
        )

        # Track explanation request
        if session_id:
            await self._track_explanation_request(card_id, user_id, session_id)

        return explanation

    async def refine_explanation(
        self,
        explanation_id: str,
        refinement_request: str,
        user_id: str
    ) -> Dict:
        """Refine an existing explanation based on user request"""
        # Get current explanation from cache
        redis_client = await self._get_redis()

        # Find the explanation by scanning cache keys
        # In production, you'd store explanation_id -> cache_key mapping
        cache_pattern = f"explanation:*:{user_id}"
        cursor = 0
        current_explanation = None

        while True:
            cursor, keys = await redis_client.scan(
                cursor,
                match=cache_pattern,
                count=100
            )

            for key in keys:
                cached_data = await redis_client.get(key)
                if cached_data:
                    data = json.loads(cached_data)
                    if data.get("id") == explanation_id:
                        current_explanation = data
                        cache_key = key
                        break

            if current_explanation or cursor == 0:
                break

        if not current_explanation:
            raise ValueError("Explanation not found")

        # Get card details
        result = await self.db.execute(
            select(Card).where(Card.id == current_explanation["card_id"])
        )
        card = result.scalar_one()

        # Analyze refinement request type
        refinement_type = self._analyze_refinement_type(refinement_request)

        # Generate refined explanation
        messages = self.refinement_prompt.format_messages(
            question=card.question,
            answer=card.answer,
            current_explanation=current_explanation["explanation"],
            refinement_request=refinement_request
        )

        response = await self.explanation_llm.ainvoke(messages)
        refined_text = response.content

        # Update explanation object
        current_explanation["explanation"] = refined_text
        current_explanation["refinement_count"] += 1
        current_explanation["last_refined_at"] = datetime.utcnow().isoformat()
        current_explanation["refinement_history"] = current_explanation.get(
            "refinement_history", [])
        current_explanation["refinement_history"].append({
            "request": refinement_request,
            "type": refinement_type,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Update cache
        await redis_client.setex(
            cache_key,
            self.explanation_cache_ttl,
            json.dumps(current_explanation)
        )

        return current_explanation

    def _get_user_level(self, difficulty: int) -> str:
        """Convert numeric difficulty to descriptive level"""
        levels = {
            1: "beginner",
            2: "elementary",
            3: "intermediate",
            4: "advanced",
            5: "expert"
        }
        return levels.get(difficulty, "intermediate")

    def _analyze_refinement_type(self, request: str) -> str:
        """Analyze what type of refinement is being requested"""
        request_lower = request.lower()

        if any(word in request_lower for word in ["simpl", "easy", "basic", "confused"]):
            return "simplify"
        elif any(word in request_lower for word in ["more", "detail", "deep", "advanced", "technical"]):
            return "deepen"
        elif any(word in request_lower for word in ["example", "show", "demonstrate", "code"]):
            return "example"
        elif any(word in request_lower for word in ["why", "how", "reason", "explain"]):
            return "clarify"
        else:
            return "general"

    async def _track_explanation_request(
        self,
        card_id: str,
        user_id: str,
        session_id: str
    ):
        """Track that user requested explanation for analytics"""
        # This could be used for improving card quality
        # and understanding which concepts need better initial answers
        pass

    async def get_explanation_stats(self, card_id: str) -> Dict:
        """Get statistics about explanations for a card"""
        redis_client = await self._get_redis()

        # Count how many times explanation was requested
        pattern = f"explanation:{card_id}:*"
        cursor = 0
        total_explanations = 0
        total_refinements = 0

        while True:
            cursor, keys = await redis_client.scan(cursor, match=pattern, count=100)

            for key in keys:
                cached_data = await redis_client.get(key)
                if cached_data:
                    data = json.loads(cached_data)
                    total_explanations += 1
                    total_refinements += data.get("refinement_count", 0)

            if cursor == 0:
                break

        return {
            "card_id": card_id,
            "total_explanation_requests": total_explanations,
            "total_refinements": total_refinements,
            "average_refinements_per_explanation": (
                total_refinements / max(total_explanations, 1)
            )
        }
