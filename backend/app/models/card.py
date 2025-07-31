from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, JSON,
    ForeignKey, Index, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .mixins import TimestampMixin
from app.config.database import Base

if TYPE_CHECKING:
    from .topic import Topic
    from .card_interaction import CardInteraction
    from .user import User


class Card(Base, AsyncAttrs, TimestampMixin):
    """Individual Q&A cards"""
    __tablename__ = "cards"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    topic_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("topics.id", ondelete="CASCADE"),
        index=True
    )

    # Content
    question: Mapped[str] = mapped_column(String(100))  # Max 100 chars
    answer: Mapped[str] = mapped_column(
        String(200))  # Max 200 chars (markdown)
    explanation: Mapped[Optional[str]] = mapped_column(
        Text)  # Extended explanation
    example: Mapped[Optional[str]] = mapped_column(Text)  # Code example

    # Metadata
    difficulty: Mapped[int] = mapped_column(Integer)
    concept_tag: Mapped[str] = mapped_column(String, index=True)
    card_type: Mapped[str] = mapped_column(
        String,
        default="standard"
    )  # standard, practice, recap

    # Generation metadata
    generation_model: Mapped[str] = mapped_column(
        String, default="gpt-3.5-turbo")
    generation_prompt_hash: Mapped[Optional[str]] = mapped_column(String)
    quality_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Analytics
    total_views: Mapped[int] = mapped_column(Integer, default=0)
    total_time_spent: Mapped[float] = mapped_column(Float, default=0.0)
    skip_rate: Mapped[float] = mapped_column(Float, default=0.0)
    save_rate: Mapped[float] = mapped_column(Float, default=0.0)

    # Relationships
    topic: Mapped["Topic"] = relationship(back_populates="cards")
    interactions: Mapped[List["CardInteraction"]] = relationship(
        back_populates="card",
        cascade="all, delete-orphan"
    )
    saved_by: Mapped[List["SavedCard"]] = relationship(
        back_populates="card",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint('difficulty >= 1 AND difficulty <= 5'),
        CheckConstraint("card_type IN ('standard', 'practice', 'recap')"),
        Index('idx_card_topic_difficulty', 'topic_id', 'difficulty'),
        Index('idx_card_concept_difficulty', 'concept_tag', 'difficulty'),
    )


class SavedCard(Base, AsyncAttrs, TimestampMixin):
    """User's saved cards for later review"""
    __tablename__ = "saved_cards"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    card_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("cards.id", ondelete="CASCADE"),
        index=True
    )

    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    folder: Mapped[Optional[str]] = mapped_column(
        String)
    tags: Mapped[List[str]] = mapped_column(
        JSON,
        default=list,
        server_default="[]"
    )
    notes: Mapped[Optional[str]] = mapped_column(Text)

    # Review status
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    last_reviewed_at: Mapped[Optional[datetime]
                             ] = mapped_column(DateTime(timezone=True))
    mastered: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="saved_cards")
    card: Mapped["Card"] = relationship(back_populates="saved_by")

    __table_args__ = (
        UniqueConstraint('user_id', 'card_id', name='uix_user_saved_card'),
        Index('idx_saved_user_folder', 'user_id', 'folder'),
    )
