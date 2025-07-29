from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from enum import Enum
from .base import BaseModel
from .associations import user_content_progress


class ContentType(str, Enum):
    LEARNING_CARD = "learning_card"
    VIDEO = "video"
    ARTICLE = "article"
    QUIZ = "quiz"
    EXERCISE = "exercise"
    DOCUMENT = "document"


class ContentStatus(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Content(BaseModel):
    """
    Base content model for all learning materials
    """
    __tablename__ = "contents"
    
    # Basic Information
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    content_type = Column(SQLEnum(ContentType), nullable=False)
    
    # Content Data
    content_data = Column(JSON)  # Flexible content storage
    metadata = Column(JSON)  # Additional metadata
    
    # Organization
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    order_index = Column(Integer, default=0)
    
    # Publishing
    status = Column(SQLEnum(ContentStatus), default=ContentStatus.DRAFT, nullable=False)
    published_at = Column(String)  # ISO datetime string
    
    # Learning Metrics
    estimated_duration_minutes = Column(Integer, default=10)
    difficulty_score = Column(Integer, default=1)  # 1-10 scale
    
    # Media
    thumbnail_url = Column(String(512))
    media_urls = Column(JSON)  # Array of media URLs
    
    # AI Generation
    is_ai_generated = Column(Boolean, default=False)
    generation_prompt = Column(Text)
    
    # Statistics
    view_count = Column(Integer, default=0)
    completion_count = Column(Integer, default=0)
    rating_sum = Column(Integer, default=0)
    rating_count = Column(Integer, default=0)
    
    # Relationships
    topic = relationship("Topic", back_populates="content_items")
    
    users_completed = relationship(
        "User",
        secondary=user_content_progress,
        back_populates="content_progress"
    )
    
    learning_sessions = relationship(
        "LearningSession",
        back_populates="current_content"
    )
    
    @property
    def average_rating(self) -> float:
        if self.rating_count == 0:
            return 0.0
        return self.rating_sum / self.rating_count
    
    def __repr__(self):
        return f"<Content(id={self.id}, title='{self.title}', type='{self.content_type}')>"


class LearningCard(Content):
    """
    Specialized learning card content
    """
    __tablename__ = "learning_cards"
    
    id = Column(Integer, ForeignKey("contents.id"), primary_key=True)
    
    # Card-specific fields
    front_content = Column(Text, nullable=False)
    back_content = Column(Text, nullable=False)
    hints = Column(JSON)  # Array of hints
    examples = Column(JSON)  # Array of examples
    
    # Spaced Repetition
    ease_factor = Column(Integer, default=250)  # 250 = 2.5
    interval_days = Column(Integer, default=1)
    repetitions = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<LearningCard(id={self.id}, title='{self.title}')>"