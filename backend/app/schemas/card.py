from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class CardBase(BaseModel):
    question: str
    answer: str
    difficulty: int
    concept_tag: str


class CardResponse(CardBase):
    id: str
    topic_id: str
    card_type: str
    total_views: int
    save_rate: float

    class Config:
        from_attributes = True


class SaveCardRequest(BaseModel):
    folder: Optional[str] = None
    tags: Optional[List[str]] = []
    notes: Optional[str] = None


class SavedCardResponse(BaseModel):
    id: str
    card_id: str
    saved_at: datetime
    folder: Optional[str]
    tags: List[str]
    notes: Optional[str]
    card: CardResponse

    class Config:
        from_attributes = True
