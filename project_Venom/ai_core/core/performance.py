"""
VENOM PERFORMANCE OPTIMIZER v2.0
==================================
Advanced caching, connection pooling, and async optimization.
"""

import asyncio
import functools
import hashlib
import json
import time
from collections import OrderedDict
from typing import Any, Callable, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp

from .logger import logger


class PerformanceCache:
    """
    LRU Cache with TTL for expensive operations.
    Thread-safe and async-compatible.
    """

    def __init__(self, max_size: int = 1000, ttl: int = 300):
        self.max_size = max_size
        self.ttl = ttl  # Time To Live in seconds
        self._cache: OrderedDict = OrderedDict()
        self._timestamps: Dict[str, float] = {}
        self._lock = asyncio.Lock()

        logger.success(f"Performance Cache initialized (size={max_size}, ttl={ttl}s)")

    def _generate_key(self, func_name: str, *args, **kwargs) -> str:
        """Generate unique cache key from function name and arguments."""
        key_data = {
            'func': func_name,
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()

    async def get(self, key: str) -> Optional[Any]:
        """Get item from cache if exists and not expired."""
        async with self._lock:
            if key not in self._cache:
                return None

            # Check TTL
            if time.time() - self._timestamps[key] > self.ttl:
                del self._cache[key]
                del self._timestamps[key]
                return None

            # Move to end (LRU)
            self._cache.move_to_end(key)
            return self._cache[key]

    async def set(self, key: str, value: Any):
        """Set item in cache."""
        async with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            else:
                if len(self._cache) >= self.max_size:
                    # Remove oldest
                    oldest_key = next(iter(self._cache))
                    del self._cache[oldest_key]
                    del self._timestamps[oldest_key]

            self._cache[key] = value
            self._timestamps[key] = time.time()

    async def clear(self):
        """Clear entire cache."""
        async with self._lock:
            self._cache.clear()
            self._timestamps.clear()

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'size': len(self._cache),
            'max_size': self.max_size,
            'ttl': self.ttl
        }


class ConnectionPool:
    """
    Connection pooling for API clients and external services.
    Reuses connections to minimize overhead.
    """

    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self._pool: asyncio.Queue = asyncio.Queue(maxsize=max_connections)
        self._active_connections = 0
        self._lock = asyncio.Lock()

        logger.success(f"Connection Pool initialized (max={max_connections})")

    async def acquire(self) -> Any:
        """Acquire a connection from pool."""
        try:
            # Try to get existing connection
            connection = self._pool.get_nowait()
            return connection
        except asyncio.QueueEmpty:
            async with self._lock:
                if self._active_connections < self.max_connections:
                    self._active_connections += 1
                    # Create new connection
                    return self._create_connection()
                else:
                    # Wait for available connection
                    return await self._pool.get()

    async def release(self, connection: Any):
        """Release connection back to pool."""
        try:
            self._pool.put_nowait(connection)
        except asyncio.QueueFull:
            # Pool is full, discard connection
            await self._close_connection(connection)
            async with self._lock:
                self._active_connections -= 1

    def _create_connection(self) -> Any:
        """Override this method to create actual connections."""
        return {"id": time.time(), "type": "mock"}

    async def _close_connection(self, connection: Any):
        """Override this method to close connections."""
        pass

    async def close_all(self):
        """Close all connections in pool."""
        while not self._pool.empty():
            connection = await self._pool.get()
            await self._close_connection(connection)
        self._active_connections = 0


class TaskExecutor:
    """
    Managed thread and process pools for CPU/IO-bound tasks.
    Auto-scaling based on system resources.
    """

    def __init__(self):
        cpu_count = mp.cpu_count()
        self.thread_pool = ThreadPoolExecutor(
            max_workers=min(32, cpu_count * 4),
            thread_name_prefix="venom_thread"
        )
        self.process_pool = ProcessPoolExecutor(
            max_workers=min(8, cpu_count),
            mp_context=mp.get_context('spawn')
        )

        # Get worker counts safely
        thread_count = getattr(self.thread_pool, '_max_workers', 'N/A')
        process_count = getattr(self.process_pool, '_max_workers', 'N/A')

        logger.success(
            f"Task Executor initialized (threads={thread_count}, "
            f"processes={process_count})"
        )

    async def run_in_thread(self, func: Callable, *args, **kwargs) -> Any:
        """Run IO-bound task in thread pool."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.thread_pool,
            functools.partial(func, *args, **kwargs)
        )

    async def run_in_process(self, func: Callable, *args, **kwargs) -> Any:
        """Run CPU-bound task in process pool."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.process_pool,
            functools.partial(func, *args, **kwargs)
        )

    def shutdown(self):
        """Shutdown all executors."""
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)
        logger.system("Task Executor shutdown complete")


# ========================
# DECORATORS
# ========================

def cache_result(ttl: int = 300):
    """Decorator to cache function results."""
    cache = PerformanceCache(ttl=ttl)

    def decorator(func: Callable):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            key = cache._generate_key(func.__name__, *args, **kwargs)

            # Try cache
            result = await cache.get(key)
            if result is not None:
                logger.print(f"Cache HIT: {func.__name__}", style="success")
                return result

            # Execute and cache
            logger.print(f"Cache MISS: {func.__name__}", style="warning")
            result = await func(*args, **kwargs)
            await cache.set(key, result)
            return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # For sync functions, use simple dict cache
            key = cache._generate_key(func.__name__, *args, **kwargs)

            if key in cache._cache:
                return cache._cache[key]

            result = func(*args, **kwargs)
            asyncio.create_task(cache.set(key, result))
            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


def retry_on_failure(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry failed async operations."""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception: Optional[Exception] = None

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}"
                        )
                        await asyncio.sleep(delay * (attempt + 1))  # Exponential backoff

            logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            if last_exception:
                raise last_exception
            raise RuntimeError(f"Function {func.__name__} failed after {max_attempts} attempts")


def measure_performance(func: Callable):
    """Decorator to measure function execution time."""
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.print(
            f"⚡ {func.__name__} executed in {elapsed:.4f}s",
            style="brain"
        )
        return result

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.print(
            f"⚡ {func.__name__} executed in {elapsed:.4f}s",
            style="brain"
        )
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


# ========================
# GLOBAL INSTANCES
# ========================

performance_cache = PerformanceCache(max_size=2000, ttl=600)
task_executor = TaskExecutor()

logger.system("🚀 Performance Optimizer v2.0 loaded")


