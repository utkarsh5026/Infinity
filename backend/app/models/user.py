"""
User model for authentication and user management
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy import String, Boolean, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.config.database import Base


class User(Base):
    """
    User model for authentication and profile management

    This model handles:
    - User authentication (email, password)
    - User profile information
    - User preferences for the dual-agent learning system
    - Relationship with conversations
    """
    __tablename__ = "users"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Authentication
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    # Account Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Profile Information
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # User Preferences for Dual-Agent System (stored as JSON)
    preferences: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    """
    Example preferences structure:
    {
        "learning_style": "visual",  # visual, logical, example-based
        "difficulty_level": "intermediate",  # beginner, intermediate, advanced
        "buddy_personality": "enthusiastic",  # calm, enthusiastic, serious, playful
        "conversation_pace": "moderate",  # slow, moderate, fast
        "language": "en",  # en, es, etc.
        "enable_hints": true,
        "enable_animations": true,
        "theme": "light"  # light, dark
    }
    """

    # Metadata
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    last_login_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # Relationships (will be defined when we create other models)
    # conversations: Mapped[list["Conversation"]] = relationship("Conversation", back_populates="user", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary (excluding sensitive data)"""
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "avatar_url": self.avatar_url,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "preferences": self.preferences,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }
