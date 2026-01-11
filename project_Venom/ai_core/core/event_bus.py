
import asyncio
from .logger import logger

class EventBus:
    """
    Robust Event Bus for system-wide communication.
    Supports Async/Sync callbacks and robust error handling.
    """
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        # logger.print(f"Subscribed: {event_type} -> {callback.__name__}", style="system")

    async def emit(self, event_type, data=None, **kwargs):
        """
        Emits an event to all subscribers.
        Safely handles errors to prevent system crash.
        """
        if event_type in self.subscribers:
            tasks = []
            for callback in self.subscribers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        tasks.append(asyncio.create_task(self._safe_async_exec(callback, data, **kwargs)))
                    else:
                        self._safe_sync_exec(callback, data, **kwargs)
                except Exception as e:
                    logger.error(f"Event Bus Emit Error ({event_type}): {e}")
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    async def _safe_async_exec(self, callback, data, **kwargs):
        try:
            # Check if callback accepts kwargs to prevent TypeError
            # Simple approach: just try calling, if fails, log it (or inspect signature)
            # For speed, we assume handlers should accept **kwargs if they expect flexibility
            # But let's be safe: catch TypeError
            await callback(data, **kwargs)
        except TypeError as e:
            if "unexpected keyword" in str(e):
                # Retry without kwargs
                try:
                    await callback(data)
                except Exception as ex:
                     logger.error(f"Handler {callback.__name__} Failed (Retry): {ex}")
            else:
                 logger.error(f"Handler {callback.__name__} Failed: {e}")
        except Exception as e:
            logger.error(f"Handler {callback.__name__} Failed: {e}")

    def _safe_sync_exec(self, callback, data, **kwargs):
        try:
            callback(data, **kwargs)
        except TypeError as e:
            if "unexpected keyword" in str(e):
                try:
                    callback(data)
                except Exception as ex:
                     logger.error(f"Handler {callback.__name__} Failed (Retry): {ex}")
            else:
                 logger.error(f"Handler {callback.__name__} Failed: {e}")
        except Exception as e:
            logger.error(f"Handler {callback.__name__} Failed: {e}")

class EventType:
    SYSTEM = "SYSTEM"
    USER_INPUT = "USER_INPUT"
    THOUGHT = "THOUGHT"
    ACTION = "ACTION"

bus = EventBus()


