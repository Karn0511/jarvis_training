"""Simple in-memory token bucket rate limiter."""
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.events = deque()

    def allow(self) -> bool:
        now = time.time()
        # Purge old events
        while self.events and now - self.events[0] > self.window:
            self.events.popleft()
        if len(self.events) >= self.max_requests:
            return False
        self.events.append(now)
        return True

rate_limiter = RateLimiter()