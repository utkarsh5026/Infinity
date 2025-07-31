import redis.asyncio as redis
import json
from loguru import logger
from typing import Optional, Any
from app.config.settings import settings
from redis.typing import ResponseT


class RedisClient:
    """
    Async Redis client for caching and session management.

    Note:
        Always call connect() before using any Redis operations.
        Call close() when shutting down the application to cleanup connections.
    """

    def __init__(self):
        self.redis_client = None

    def has_client(self) -> bool:
        """Check if Redis client is connected"""
        return self.redis_client is not None

    async def connect(self):
        """Connect to Redis"""
        try:
            self.redis_client = await redis.from_url(
                settings.REDIS_URL,
                decode_responses=True
            )
            await self.redis_client.ping()
            logger.success("Connected to Redis successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.redis_client = None

    async def get(self, key: str) -> Optional[ResponseT]:
        """
        Retrieve and deserialize value from Redis by key.

        Automatically deserializes JSON data back to Python objects.
        Returns None if key doesn't exist or if not connected.

        Args:
            key (str): The Redis key to retrieve

        Returns:
            Optional[Any]: Deserialized value or None if not found/error
        """
        if not self.redis_client:
            return None

        try:
            value = await self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis GET error: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """
        Store value in Redis with automatic JSON serialization and TTL.

        Serializes Python objects to JSON before storing. Uses default TTL
        from settings if not specified.

        Args:
            key (str): Redis key to store under
            value (Any): Python object to store (must be JSON serializable)
            ttl (Optional[int]): Time to live in seconds. Uses CACHE_TTL if None

        Returns:
            bool: True if stored successfully, False otherwise
        """
        if not self.redis_client:
            return False

        try:
            ttl = ttl or settings.CACHE_TTL
            serialized_value = json.dumps(value, default=str)
            return await self.redis_client.setex(key, ttl, serialized_value)
        except Exception as e:
            logger.error(f"Redis SET error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete key from Redis.

        Args:
            key (str): The Redis key to delete

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        if not self.redis_client:
            return False

        try:
            return bool(await self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"Redis DELETE error: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.redis_client:
            return False

        try:
            return bool(await self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Redis EXISTS error: {e}")
            return False

    async def flush_all(self) -> bool:
        """
        Delete all keys from Redis database.

        ⚠️  WARNING: This operation removes ALL data from the Redis database.
        Use with extreme caution, especially in production environments.

        Returns:
            bool: True if operation succeeded, False otherwise
        """
        if not self.redis_client:
            return False

        try:
            return await self.redis_client.flushall()
        except Exception as e:
            logger.error(f"Redis FLUSHALL error: {e}")
            return False

    async def close(self):
        """
        Close the Redis connection gracefully.

        Should be called during application shutdown to ensure proper cleanup
        of network connections.
        """
        if self.redis_client:
            await self.redis_client.close()


redis_client = RedisClient()
