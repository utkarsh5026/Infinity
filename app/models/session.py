from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, JSON, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel


class LearningSession(BaseModel):
    """
    Learning session tracking
    """
    __tablename__ = "learning_sessions"
    
    # Session Information
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    current_content_id = Column(Integer, ForeignKey("contents.id"), nullable=True)
    
    # Session Data
    session_name = Column(String(255))
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer, default=0)
    
    # Progress Tracking
    items_completed = Column(Integer, default=0)
    items_total = Column(Integer, default=0)
    completion_percentage = Column(Float, default=0.0)
    
    # Performance Metrics
    correct_answers = Column(Integer, default=0)
    total_answers = Column(Integer, default=0)
    accuracy_percentage = Column(Float, default=0.0)
    
    # Session State
    is_completed = Column(Boolean, default=False)
    is_paused = Column(Boolean, default=False)
    session_data = Column(JSON)  # Additional session state
    
    # Relationships
    user = relationship("User", back_populates="learning_sessions")
    topic = relationship("Topic", back_populates="learning_sessions")
    current_content = relationship("Content", back_populates="learning_sessions")
    progress_entries = relationship(
        "SessionProgress", 
        back_populates="session",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<LearningSession(id={self.id}, user_id={self.user_id}, topic_id={self.topic_id})>"


class SessionProgress(BaseModel):
    """
    Detailed progress tracking within a session
    """
    __tablename__ = "session_progress"
    
    # Progress Information
    session_id = Column(Integer, ForeignKey("learning_sessions.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    
    # Progress Data
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    time_spent_seconds = Column(Integer, default=0)
    
    # Performance
    is_completed = Column(Boolean, default=False)
    is_correct = Column(Boolean, nullable=True)  # For quiz/exercise content
    attempts_count = Column(Integer, default=0)
    score = Column(Float, nullable=True)  # 0.0 to 1.0
    
    # User Response Data
    user_response = Column(JSON)  # Store user answers/responses
    feedback_data = Column(JSON)  # Store feedback/hints used
    
    # Spaced Repetition (for learning cards)
    ease_factor = Column(Float, default=2.5)
    interval_days = Column(Integer, default=1)
    next_review_date = Column(DateTime(timezone=True))
    
    # Relationships
    session = relationship("LearningSession", back_populates="progress_entries")
    content = relationship("Content")
    
    def __repr__(self):
        return f"<SessionProgress(id={self.id}, session_id={self.session_id}, content_id={self.content_id})>"