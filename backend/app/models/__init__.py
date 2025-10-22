"""
Database models for Infinity Learning Platform
"""
from app.models.user import User
from app.models.mixins import TimestampMixin

__all__ = ["User", "TimestampMixin"]
