"""
Script to create database tables
"""
import asyncio
from app.config.database import engine, Base
from app.models.user import User  # Import all models here


async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())
