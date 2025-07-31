from datetime import datetime
from sqlalchemy import (
    DateTime,
    String
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
import uuid


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class UUIDPrimaryKeyMixin:
    """Mixin for UUID primary key"""
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
