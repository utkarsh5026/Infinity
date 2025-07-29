from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, JSON, Text, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from .base import BaseModel


class EventType(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    CONTENT_VIEW = "content_view"
    CONTENT_COMPLETE = "content_complete"
    QUIZ_ATTEMPT = "quiz_attempt"
    SEARCH = "search"
    BOOKMARK = "bookmark"
    RATING = "rating"
    COMMENT = "comment"
    SHARE = "share"
    ERROR = "error"


class UserAnalytics(BaseModel):
    """
    Aggregated user analytics and learning metrics
    """
    __tablename__ = "user_analytics"
    
    # User Reference
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Learning Metrics
    total_study_time_minutes = Column(Integer, default=0)
    total_content_completed = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    current_streak_days = Column(Integer, default=0)
    longest_streak_days = Column(Integer, default=0)
    
    # Performance Metrics
    average_accuracy = Column(Float, default=0.0)
    total_correct_answers = Column(Integer, default=0)
    total_attempts = Column(Integer, default=0)
    
    # Progress Metrics
    topics_started = Column(Integer, default=0)
    topics_completed = Column(Integer, default=0)
    skill_points = Column(Integer, default=0)
    current_level = Column(Integer, default=1)
    
    # Engagement Metrics
    login_count = Column(Integer, default=0)
    last_active_date = Column(DateTime(timezone=True))
    last_streak_update = Column(DateTime(timezone=True))
    
    # Learning Patterns (JSON data for complex analytics)
    learning_patterns = Column(JSON)  # Study times, preferred content types, etc.
    weak_areas = Column(JSON)  # Topics that need improvement
    strong_areas = Column(JSON)  # Topics with high performance
    
    # Achievements
    achievements = Column(JSON)  # Array of achievement IDs/data
    badges = Column(JSON)  # Array of badge data
    
    # Relationships
    user = relationship("User", back_populates="analytics")
    
    def __repr__(self):
        return f"<UserAnalytics(id={self.id}, user_id={self.user_id}, level={self.current_level})>"


class InteractionEvent(BaseModel):
    """
    Individual user interaction events for detailed analytics
    """
    __tablename__ = "interaction_events"
    
    # Event Information
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_type = Column(SQLEnum(EventType), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Context Information
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    session_id = Column(Integer, ForeignKey("learning_sessions.id"), nullable=True)
    
    # Event Data
    event_data = Column(JSON)  # Flexible event-specific data
    metadata = Column(JSON)  # Additional context (device, browser, etc.)
    
    # Performance Context
    duration_seconds = Column(Integer, nullable=True)
    success = Column(Boolean, nullable=True)
    score = Column(Float, nullable=True)
    
    # System Information
    ip_address = Column(String(45))  # IPv6 compatible
    user_agent = Column(String(512))
    device_type = Column(String(50))  # mobile, tablet, desktop
    
    # Relationships
    user = relationship("User", back_populates="interaction_events")
    content = relationship("Content")
    topic = relationship("Topic")
    session = relationship("LearningSession")
    
    def __repr__(self):
        return f"<InteractionEvent(id={self.id}, user_id={self.user_id}, type='{self.event_type}')>"