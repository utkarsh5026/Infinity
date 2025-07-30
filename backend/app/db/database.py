from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Convert SQLite URL to async format
async_database_url = settings.DATABASE_URL.replace(
    "sqlite:///", "sqlite+aiosqlite:///")

# Create async SQLAlchemy engine
engine = create_async_engine(
    async_database_url,
    echo=False,  # Set to True for SQL query logging
)

# Create async SessionLocal class
SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

# Create Base class
Base = declarative_base()

# Async dependency to get database session


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
