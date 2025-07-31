from typing import List, Optional, Dict
from pydantic import BaseModel


class TopicBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None


class TopicResponse(TopicBase):
    id: str
    slug: str
    icon_url: Optional[str]
    cover_image_url: Optional[str]
    difficulty_range: Dict[str, int]
    estimated_cards: int
    popularity_score: float

    class Config:
        from_attributes = True


class TopicListResponse(BaseModel):
    topics: List[TopicResponse]
    total: int
    skip: int
    limit: int


class TopicDetailResponse(TopicResponse):
    core_concepts: List[str]
    prerequisites: List[str]
    card_stats: Dict
