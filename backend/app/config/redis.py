import redis.asyncio as redis
import json
from loguru import logger
from typing import Optional, Any
from app.config.settings import settings
from redis.typing import ResponseT


class RedisClient:
    """
    Async Redis client for caching and session management
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
        """Get value by key"""
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
        """Set key-value pair with optional TTL"""
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
        """Delete key"""
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
        """Flush all keys (use with caution)"""
        if not self.redis_client:
            return False

        try:
            return await self.redis_client.flushall()
        except Exception as e:
            logger.error(f"Redis FLUSHALL error: {e}")
            return False

    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()


redis_client = RedisClient()
