from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from .base import BaseModel
from .associations import user_topic_association


class TopicDifficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class TopicCategory(str, Enum):
    PROGRAMMING = "programming"
    MATHEMATICS = "mathematics"
    SCIENCE = "science"
    LANGUAGE = "language"
    BUSINESS = "business"
    ARTS = "arts"
    HISTORY = "history"
    OTHER = "other"


class Topic(BaseModel):
    """
    Learning topics and categories
    """
    __tablename__ = "topics"

    # Basic Information
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    short_description = Column(String(500))

    # Classification
    category = Column(SQLEnum(TopicCategory),
                      default=TopicCategory.OTHER, nullable=False)
    difficulty = Column(SQLEnum(TopicDifficulty),
                        default=TopicDifficulty.BEGINNER, nullable=False)
    tags = Column(Text)  # JSON string of tags

    # Hierarchy
    parent_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    order_index = Column(Integer, default=0)

    # Content
    thumbnail_url = Column(String(512))
    estimated_duration_minutes = Column(Integer, default=60)

    # Statistics
    enrollment_count = Column(Integer, default=0)
    completion_rate = Column(Integer, default=0)  # Percentage

    # Relationships
    parent = relationship("Topic", remote_side="Topic.id",
                          back_populates="children")
    children = relationship(
        "Topic", back_populates="parent", cascade="all, delete-orphan")

    enrolled_users = relationship(
        "User",
        secondary=user_topic_association,
        back_populates="topics"
    )

    content_items = relationship(
        "Content",
        back_populates="topic",
        cascade="all, delete-orphan"
    )

    learning_sessions = relationship(
        "LearningSession",
        back_populates="topic",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Topic(id={self.id}, title='{self.title}', category='{self.category}')>"
