"""
Database model mixins for common functionality
"""
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """
    Mixin that adds created_at and updated_at timestamp fields to models.

    Usage:
        class MyModel(Base, TimestampMixin):
            # ... your model fields
            pass
    """
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
