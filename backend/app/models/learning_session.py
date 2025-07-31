from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import (
    String,
    Integer,
    Float,
    DateTime,
    JSON,
    ForeignKey,
    Index,
    CheckConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.sql import func
from .mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.config.database import Base

if TYPE_CHECKING:
    from .user import User
    from .topic import Topic
    from .card_interaction import CardInteraction


class LearningSession(Base, AsyncAttrs, TimestampMixin, UUIDPrimaryKeyMixin):
    """
    User learning sessions.

    Tracks user progress through learning sessions, including the cards
    they've viewed, the time spent, and the concepts they've covered.
    """
    __tablename__ = "learning_sessions"

    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )

    topic_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("topics.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    session_type: Mapped[str] = mapped_column(
        String,
        default="standard"
    )  # standard, review, practice
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True))

    cards_viewed: Mapped[int] = mapped_column(Integer, default=0)
    total_time_seconds: Mapped[float] = mapped_column(Float, default=0.0)

    current_card_index: Mapped[int] = mapped_column(Integer, default=0)
    card_queue: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        server_default="[]"
    )  # List of card IDs
    asked_questions: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        server_default="[]"
    )  # For duplicate prevention
    covered_concepts: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        server_default="[]"
    )

    # Analytics
    engagement_score: Mapped[float] = mapped_column(Float, default=0.0)
    completion_rate: Mapped[float] = mapped_column(Float, default=0.0)

    user: Mapped["User"] = relationship(back_populates="learning_sessions")
    topic: Mapped[Optional["Topic"]] = relationship(
        back_populates="learning_sessions")
    card_interactions: Mapped[List["CardInteraction"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("session_type IN ('standard', 'review', 'practice')"),
        Index('idx_session_user_started', 'user_id', 'started_at'),
    )
