from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import (
    String, Integer, Boolean, Text, CheckConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
import uuid
from .mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.config.database import Base

if TYPE_CHECKING:
    from .card_interaction import CardInteraction
    from .learning_session import LearningSession
    from .card import SavedCard


class User(Base, AsyncAttrs, TimestampMixin, UUIDPrimaryKeyMixin):
    """User model with learning preferences"""
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

    full_name: Mapped[Optional[str]] = mapped_column(String)
    avatar_url: Mapped[Optional[str]] = mapped_column(String)
    bio: Mapped[Optional[str]] = mapped_column(Text)

    preferred_difficulty: Mapped[int] = mapped_column(
        Integer,
        default=3,
        server_default="3"
    )
    learning_style: Mapped[str] = mapped_column(
        String,
        default="mixed",
        server_default="mixed"
    )
    daily_goal: Mapped[int] = mapped_column(
        Integer,
        default=20,
        server_default="20"
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    notification_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    learning_sessions: Mapped[List["LearningSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    card_interactions: Mapped[List["CardInteraction"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    saved_cards: Mapped[List["SavedCard"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            'preferred_difficulty >= 1 AND preferred_difficulty <= 5'),
        CheckConstraint(
            "learning_style IN ('visual', 'textual', 'practical', 'mixed')"),
    )
