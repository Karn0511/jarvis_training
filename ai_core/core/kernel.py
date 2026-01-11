
import asyncio
import importlib
from .event_bus import bus, EventType
from .logger import logger

class VenomKernel:
    """
    The Central Nervous System of Project Venom v2.
    Integrates EventBus, Logger, and Organ Management.
    """
    def __init__(self):
        self.organs = {}
        self.running = False
        self.state = "BOOT"
        
        # Subscribe Kernel's own handlers
        bus.subscribe("SHUTDOWN", self.handle_shutdown)
        bus.subscribe("STARTUP", self.handle_startup)

    def register_organ(self, name, organ_instance):
        """Connects a new organ to the kernel."""
        try:
            self.organs[name] = organ_instance
            if hasattr(organ_instance, "initialize"):
                 # Allow organs to set up their own subscriptions
                organ_instance.initialize(bus)
            
            logger.success(f"Organ Attached: {name}")
        except Exception as e:
            logger.error(f"Kernel Rejection ({name}): {e}")

    def get_organ(self, name):
        return self.organs.get(name)

    async def handle_shutdown(self, _, **kwargs):
        """Graceful Shutdown Sequence."""
        logger.system("Initiating Shutdown Sequence...")
        self.running = False

    async def handle_startup(self, _, **kwargs):
        """System Startup Sequence."""
        self.set_state("ALIVE")
        logger.system("All Organs Reporting Ready.")

    def set_state(self, new_state):
        self.state = new_state
        # logger.print(f"KERNEL STATE >> {new_state}", style="brain")

    async def start(self):
        """Main Life Loop."""
        self.running = True
        logger.print("VENOM SYSTEM KERNEL v2.0 - ONLINE", style="success")
        
        # Trigger startup events
        await bus.emit("STARTUP", category=EventType.SYSTEM)

        while self.running:
            await asyncio.sleep(0.1)  # Keep the loop alive
            
        logger.print("VENOM SYSTEM OFFLINE", style="critical")


