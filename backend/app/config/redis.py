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
        self._redis_connection = None

    def is_connected(self) -> bool:
        """Check if Redis client is connected"""
        return self._redis_connection is not None

    def get_raw_redis_client(self):
        """Get the internal Redis client for advanced operations"""
        return self._redis_connection

    async def connect_to_redis(self):
        """Connect to Redis"""
        try:
            self._redis_connection = await redis.from_url(
                settings.REDIS_URL,
                decode_responses=True
            )
            await self._redis_connection.ping()
            logger.success("Connected to Redis successfully")
        except Exception as redis_connection_error:
            logger.error(f"Failed to connect to Redis: {redis_connection_error}")
            self._redis_connection = None

    async def get_value(self, redis_key: str) -> Optional[ResponseT]:
        """
        Retrieve and deserialize value from Redis by key.

        Automatically deserializes JSON data back to Python objects.
        Returns None if key doesn't exist or if not connected.
        """
        if not self._redis_connection:
            return None

        try:
            cached_value = await self._redis_connection.get(redis_key)
            if cached_value:
                return json.loads(cached_value)
            return None
        except Exception as redis_get_error:
            logger.error(f"Redis GET error: {redis_get_error}")
            return None

    async def set_value(self, redis_key: str, data_to_cache: Any, expiration_seconds: Optional[int] = None) -> bool:
        """
        Store value in Redis with automatic JSON serialization and TTL.

        Serializes Python objects to JSON before storing. Uses default TTL
        from settings if not specified.
        """
        if not self._redis_connection:
            return False

        try:
            time_to_live = expiration_seconds or settings.CACHE_TTL
            serialized_data = json.dumps(data_to_cache, default=str)
            return await self._redis_connection.setex(redis_key, time_to_live, serialized_data)
        except Exception as redis_set_error:
            logger.error(f"Redis SET error: {redis_set_error}")
            return False

    async def delete_key(self, redis_key: str) -> bool:
        """
        Delete key from Redis.
        """
        if not self._redis_connection:
            return False

        try:
            return bool(await self._redis_connection.delete(redis_key))
        except Exception as redis_delete_error:
            logger.error(f"Redis DELETE error: {redis_delete_error}")
            return False

    async def key_exists(self, redis_key: str) -> bool:
        """Check if key exists"""
        if not self._redis_connection:
            return False

        try:
            return bool(await self._redis_connection.exists(redis_key))
        except Exception as redis_exists_error:
            logger.error(f"Redis EXISTS error: {redis_exists_error}")
            return False

    async def flush_entire_database(self) -> bool:
        """
        Delete all keys from Redis database.
        """
        if not self._redis_connection:
            return False

        try:
            return await self._redis_connection.flushall()
        except Exception as redis_flush_error:
            logger.error(f"Redis FLUSHALL error: {redis_flush_error}")
            return False

    async def close_connection(self):
        """
        Close the Redis connection gracefully.

        Should be called during application shutdown to ensure proper cleanup
        of network connections.
        """
        if self._redis_connection:
            await self._redis_connection.close()


redis_client = RedisClient()
