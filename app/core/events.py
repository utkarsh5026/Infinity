import logging
from fastapi import FastAPI
from app.config.database import create_tables
from app.config.redis import redis_client
from app.config.logging import setup_logging

logger = logging.getLogger(__name__)


async def startup_event():
    """
    Application startup event handler
    """
    logger.info("Starting up Infinity Learning Platform...")

    # Setup logging
    setup_logging()

    # Create database tables
    try:
        create_tables()
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

    # Test Redis connection
    try:
        if redis_client.redis_client:
            redis_client.redis_client.ping()
            logger.info("Redis connection established")
        else:
            logger.warning("Redis client not available")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}")

    # Initialize any background services here
    # await init_background_services()

    logger.info("Application startup completed successfully")


async def shutdown_event():
    """
    Application shutdown event handler
    """
    logger.info("Shutting down Infinity Learning Platform...")

    # Close Redis connections
    try:
        if redis_client.redis_client:
            redis_client.redis_client.close()
            logger.info("Redis connections closed")
    except Exception as e:
        logger.error(f"Error closing Redis connections: {e}")

    # Cleanup any background services
    # await cleanup_background_services()

    logger.info("Application shutdown completed")


def setup_events(app: FastAPI) -> None:
    """
    Setup startup and shutdown events
    """
    app.add_event_handler("startup", startup_event)
    app.add_event_handler("shutdown", shutdown_event)

    logger.info("Event handlers registered")
