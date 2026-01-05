"""
Intelligent Caching System with Redis fallback
"""
import json
import hashlib
from typing import Any, Optional, Dict
import time

try:
    import aioredis  # type: ignore
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from core.config import settings


class CacheManager:
    """Smart cache with Redis or in-memory fallback"""

    def __init__(self):
        self.redis = None
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        self.initialized = False

    async def initialize(self):
        """Initialize Redis connection"""
        if settings.REDIS_URL and REDIS_AVAILABLE:
            try:
                self.redis = await aioredis.create_redis_pool(settings.REDIS_URL)  # type: ignore
                print("✅ Redis cache connected")
            except Exception as e:
                print(f"⚠️  Redis unavailable, using memory cache: {e}")
        else:
            print("ℹ️  Using in-memory cache")

        self.initialized = True

    def _generate_key(self, prefix: str, data: Any) -> str:
        """Generate cache key from data"""
        data_str = json.dumps(data, sort_keys=True)
        hash_obj = hashlib.sha256(data_str.encode())
        return f"{prefix}:{hash_obj.hexdigest()[:16]}"

    async def get(self, key: str) -> Optional[Any]:
        """Get from cache"""
        if self.redis:
            value = await self.redis.get(key)
            return json.loads(value) if value else None
        entry = self.memory_cache.get(key)
        if not entry:
            return None
        if entry['expires_at'] < time.time():
            self.memory_cache.pop(key, None)
            return None
        return entry['value']

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set in cache with TTL"""
        ttl = ttl or settings.CACHE_TTL

        if self.redis:
            await self.redis.setex(key, ttl, json.dumps(value))
            return
        # In-memory with explicit expiry timestamp & simple size cap
        if len(self.memory_cache) > 5000:
            # Drop oldest entries heuristically
            oldest_keys = sorted(self.memory_cache.items(), key=lambda kv: kv[1]['expires_at'])[:100]
            for k, _ in oldest_keys:
                self.memory_cache.pop(k, None)
        self.memory_cache[key] = {"value": value, "expires_at": time.time() + ttl}

    async def _expire_key(self, key: str, ttl: int):
        """Deprecated: expiry handled inline (kept for compatibility)."""
        return

    async def delete(self, key: str):
        """Delete from cache"""
        if self.redis:
            await self.redis.delete(key)
        else:
            self.memory_cache.pop(key, None)

    async def clear_all(self):
        """Clear all cache"""
        if self.redis:
            await self.redis.flushdb()
        else:
            self.memory_cache.clear()

# Global cache instance
cache = CacheManager()
