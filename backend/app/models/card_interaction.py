from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import (
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    Index,
    UniqueConstraint,
    CheckConstraint,
    ForeignKey
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid
from .mixins import TimestampMixin
from app.config.database import Base

if TYPE_CHECKING:
    from .user import User
    from .card import Card
    from .learning_session import LearningSession


class CardInteraction(Base, AsyncAttrs, TimestampMixin):
    """Detailed tracking of user interactions with cards"""
    __tablename__ = "card_interactions"

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
    session_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("learning_sessions.id", ondelete="CASCADE"),
        index=True
    )

    # Interaction data
    viewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    time_spent_seconds: Mapped[float] = mapped_column(Float)
    answer_revealed: Mapped[bool] = mapped_column(Boolean, default=False)

    # User actions
    action: Mapped[str] = mapped_column(String)  # view, skip, save, master
    confidence_rating: Mapped[Optional[int]] = mapped_column(Integer)  # 1-5

    # Spaced repetition data
    repetition_number: Mapped[int] = mapped_column(Integer, default=1)
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)
    next_review_date: Mapped[Optional[datetime]
                             ] = mapped_column(DateTime(timezone=True))

    # Relationships
    user: Mapped["User"] = relationship(back_populates="card_interactions")
    card: Mapped["Card"] = relationship(back_populates="interactions")
    session: Mapped["LearningSession"] = relationship(
        back_populates="card_interactions")

    __table_args__ = (
        UniqueConstraint('user_id', 'card_id', 'session_id',
                         name='uix_user_card_session'),
        CheckConstraint("action IN ('view', 'skip', 'save', 'master')"),
        CheckConstraint(
            'confidence_rating IS NULL OR (confidence_rating >= 1 AND confidence_rating <= 5)'),
        Index('idx_interaction_user_viewed', 'user_id', 'viewed_at'),
    )
