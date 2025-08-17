from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class GenerationMode(str, Enum):
    STANDARD = "standard"
    RAPID_FIRE = "rapid_fire"
    DEEP_DIVE = "deep_dive"
    PRACTICE = "practice"


class QACard(BaseModel):
    """Single Q&A card model"""
    question: str = Field(..., max_length=80)
    answer: str = Field(..., max_length=300)
    difficulty: int = Field(..., ge=1, le=5)
    concept_tag: str


class QABatch(BaseModel):
    """Batch of Q&A cards"""
    cards: List[QACard]
    topic: str
    generated_at: datetime = Field(default_factory=datetime.now)
    session_context: str


class StartSessionRequest(BaseModel):
    topic: str
    category: Optional[str] = "general"
    mode: GenerationMode = GenerationMode.STANDARD


class StartSessionResponse(BaseModel):
    session_id: str
    initial_cards: List[Dict]
    total_concepts: int


class CardResponse(BaseModel):
    id: str
    question: str
    answer: str
    difficulty: int
    concept_tag: str


class SessionMetricsUpdate(BaseModel):
    card_id: str
    time_spent: float = Field(..., ge=0)
    answer_revealed: bool = False
    action: str = Field(..., pattern="^(view|skip|save|master)$")
    confidence_rating: Optional[int] = Field(None, ge=1, le=5)


class SessionStatsResponse(BaseModel):
    session_id: str
    cards_viewed: int
    cards_mastered: int
    total_time_seconds: float
    average_time_per_card: float
    completion_rate: float
    engagement_score: float
