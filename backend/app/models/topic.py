from typing import Optional, TYPE_CHECKING
from sqlalchemy import (
    String, Integer, Text, JSON
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from .mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.config.database import Base

if TYPE_CHECKING:
    from .card import Card
    from .learning_session import LearningSession


class Topic(Base, AsyncAttrs, TimestampMixin, UUIDPrimaryKeyMixin):
    """Learning topics and categories"""
    __tablename__ = "topics"

    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    category: Mapped[str] = mapped_column(String, index=True)

    description: Mapped[Optional[str]] = mapped_column(Text)

    difficulty_range: Mapped[dict] = mapped_column(
        JSON,
        default={"min": 1, "max": 5}
    )
    estimated_cards: Mapped[int] = mapped_column(Integer, default=30)

    topic_structure: Mapped[Optional[dict]] = mapped_column(JSON)
    core_concepts: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        server_default="[]"
    )
    prerequisites: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        server_default="[]"
    )

    cards: Mapped[list["Card"]] = relationship(
        back_populates="topic",
        cascade="all, delete-orphan"
    )
    learning_sessions: Mapped[list["LearningSession"]] = relationship(
        back_populates="topic"
    )
