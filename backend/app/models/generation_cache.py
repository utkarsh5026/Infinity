from datetime import datetime
from sqlalchemy import (
    String, Integer, DateTime, JSON, Index
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.sql import func
from .mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.config.database import Base


class GenerationCache(Base, AsyncAttrs, TimestampMixin, UUIDPrimaryKeyMixin):
    """
    Cache for LLM generations to reduce costs.

    Stores responses from LLM models to reduce API calls and costs.
    It is used to cache the responses from the LLM models to reduce the number of API calls and costs.
    """
    __tablename__ = "generation_cache"

    topic: Mapped[str] = mapped_column(String, index=True)
    prompt_hash: Mapped[str] = mapped_column(String, unique=True, index=True)
    model: Mapped[str] = mapped_column(String)

    response_data: Mapped[dict] = mapped_column(JSON)
    token_count: Mapped[int] = mapped_column(Integer)
    generation_time_ms: Mapped[int] = mapped_column(Integer)

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True
    )
    hit_count: Mapped[int] = mapped_column(Integer, default=0)
    last_accessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        Index('idx_cache_topic_expires', 'topic', 'expires_at'),
    )
