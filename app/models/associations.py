from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.sql import func
from app.config.database import Base

# User-Topic association table (many-to-many)
user_topic_association = Table(
    'user_topic_associations',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('topic_id', Integer, ForeignKey('topics.id'), nullable=False),
    Column('enrolled_at', DateTime(timezone=True), server_default=func.now()),
    Column('completed_at', DateTime(timezone=True), nullable=True),
    Column('is_favorite', Boolean, default=False),
    Column('progress_percentage', Float, default=0.0),
    Column('last_accessed_at', DateTime(timezone=True)),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now())
)

# User-Content progress association table (many-to-many)
user_content_progress = Table(
    'user_content_progress',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('content_id', Integer, ForeignKey('contents.id'), nullable=False),
    Column('completed_at', DateTime(timezone=True), server_default=func.now()),
    Column('is_bookmarked', Boolean, default=False),
    Column('rating', Integer, nullable=True),  # 1-5 stars
    Column('time_spent_seconds', Integer, default=0),
    Column('completion_percentage', Float, default=0.0),
    Column('last_accessed_at', DateTime(timezone=True)),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now())
)