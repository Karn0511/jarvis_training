"""Ultra-lightweight local LLM router (zero-cost) with caching, concurrency and rate limiting."""
from typing import Dict, Any, Optional
import asyncio
from core.config import settings
from core.cache import cache
from .rate_limiter import rate_limiter

class LLMRouter:
    def __init__(self, max_concurrent: int = 4):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.local_model = self._get_local_model()
        self.request_count = 0

    def _get_local_model(self):
        class LocalModel:
            async def generate(self, prompt: str) -> str:
                # Simple deterministic pseudo-response to avoid external cost
                truncated = prompt.strip().replace('\n', ' ')[:256]
                return f"Local Response: {truncated}"
        return LocalModel()

    async def query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        # Rate limit
        if not rate_limiter.allow():
            return {"answer": "Rate limit exceeded. Retry later.", "model": "local-llama", "cached": False}

        cache_key = None
        if use_cache:
            cache_key = cache._generate_key("llm", {"p": prompt, "s": system_prompt})
            cached = await cache.get(cache_key)
            if cached:
                return {**cached, "cached": True}

        async with self.semaphore:
            self.request_count += 1
            answer = await self.local_model.generate(prompt if not system_prompt else f"{system_prompt}\n{prompt}")
            response = {"answer": answer, "model": "local-llama"}
            if use_cache and cache_key:
                await cache.set(cache_key, response)
            return {**response, "cached": False}

llm_router = LLMRouter()
