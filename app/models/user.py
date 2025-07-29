from sqlalchemy import Column, String, Boolean, Integer, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum
from .base import BaseModel
from .associations import user_topic_association, user_content_progress


class UserRole(str, Enum):
    STUDENT = "student"
    EDUCATOR = "educator"
    ADMIN = "admin"


class LearningStyle(str, Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"


class User(BaseModel):
    """
    User model with preferences and learning data
    """
    __tablename__ = "users"

    # Basic Information
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    avatar_url = Column(String(512))

    # Role and Status
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_verified = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)

    # Learning Preferences
    learning_style = Column(SQLEnum(LearningStyle),
                            default=LearningStyle.VISUAL)
    # beginner, intermediate, advanced
    preferred_difficulty = Column(String(20), default="intermediate")
    daily_goal_minutes = Column(Integer, default=30)

    # Profile Information
    bio = Column(Text)
    interests = Column(Text)  # JSON string of interests
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")

    # Account Status
    last_login_at = Column(DateTime(timezone=True))
    email_verified_at = Column(DateTime(timezone=True))
    premium_expires_at = Column(DateTime(timezone=True))

    # Relationships
    topics = relationship(
        "Topic",
        secondary=user_topic_association,
        back_populates="enrolled_users",
        lazy="dynamic"
    )

    learning_sessions = relationship(
        "LearningSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    analytics = relationship(
        "UserAnalytics",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    interaction_events = relationship(
        "InteractionEvent",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    content_progress = relationship(
        "Content",
        secondary=user_content_progress,
        back_populates="users_completed"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
