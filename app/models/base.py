from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from app.config.database import Base


class TimestampMixin:
    """
    Mixin for adding timestamp fields to models
    """
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BaseModel(Base, TimestampMixin):
    """
    Base model class with common fields
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    @declared_attr
    def __tablename__(cls):
        """
        Generate table name from class name
        """
        return cls.__name__.lower() + 's'

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
