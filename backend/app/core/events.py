from fastapi import FastAPI
from app.config.database import create_tables
from app.config.redis import redis_client
from loguru import logger


async def startup_event():
    """
    Application startup event handler
    """
    logger.info("Starting up Infinity Learning Platform...")

    try:
        await create_tables()
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

    try:
        if redis_client.has_client():
            await redis_client.connect()
            logger.info("Redis connection established")
        else:
            logger.warning("Redis client not available")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}")

    logger.info("Application startup completed successfully")


async def shutdown_event():
    """
    Application shutdown event handler
    """
    logger.info("Shutting down Infinity Learning Platform...")

    try:
        if redis_client.has_client():
            await redis_client.close()
            logger.info("Redis connections closed")
    except Exception as e:
        logger.error(f"Error closing Redis connections: {e}")

    logger.info("Application shutdown completed")


def setup_events(app: FastAPI) -> None:
    """
    Setup startup and shutdown events
    """
    app.add_event_handler("startup", startup_event)
    app.add_event_handler("shutdown", shutdown_event)

    logger.info("Event handlers registered")
