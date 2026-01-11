import os
from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

# Force load .env from project root (go up 2 levels from ai_core/core)
env_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"
)
if not os.path.exists(env_path):
    print(f"CRITICAL: .env file not found at {env_path}")
else:
    load_dotenv(env_path, override=True)
    if not os.getenv("GEMINI_API_KEY"):
        print("CRITICAL: GEMINI_API_KEY NOT FOUND IN .env")
    else:
        print("GEMINI_API_KEY LOADED SUCCESSFULLY")


class Settings(BaseSettings):
    PROJECT_NAME: str = "Project Venom"
    VERSION: str = "2.0.0-TURBO"

    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "storage")
    MEMORY_DIR: str = os.path.join(DATA_DIR, "neural/memory")

    # AI Keys (Use Field to force lookup)
    GEMINI_API_KEY: str
    OPENAI_API_KEY: str = ""

    # System
    DEBUG_MODE: bool = True
    VOICE_ENABLED: bool = True
    VENOM_BOOST: bool = True  # TURBO MODE: Maximum performance

    # ========================
    # ULTIMATE PERFORMANCE SETTINGS
    # ========================

    # Advanced Cache Configuration
    CACHE_ENABLED: bool = True
    CACHE_SIZE: int = 3000  # Increased cache capacity
    CACHE_TTL: int = 900  # Extended cache lifetime (15 min)

    # High-Performance Connection Pooling
    MAX_CONNECTIONS: int = 30  # More connections
    CONNECTION_TIMEOUT: int = 45

    # Maximum Parallel Processing
    MAX_WORKERS_THREADS: int = 48  # Increased thread workers
    MAX_WORKERS_PROCESSES: int = 12  # More process workers
    MAX_CONCURRENT_TASKS: int = 20  # More concurrent tasks

    # Memory Optimization
    MEMORY_WORKING_SIZE: int = 30  # Larger working memory
    MEMORY_LTM_BATCH_SIZE: int = 100  # Bigger batch processing
    MEMORY_CLEANUP_INTERVAL: int = 600  # Cleanup every 10 min

    # Advanced Response Optimization
    ENABLE_SMART_ROUTING: bool = True
    ENABLE_PATTERN_MATCHING: bool = True
    BATCH_PROCESSING: bool = True
    BATCH_SIZE: int = 10  # Larger batch size
    BATCH_TIMEOUT: float = 1.5  # Faster timeout

    # Model Selection (Optimized)
    FAST_MODEL: str = "gemini-3-flash-preview"
    SMART_MODEL: str = "gemini-3-pro-preview"
    AUTO_MODEL_SELECTION: bool = True  # Intelligent model routing

    # Streaming & Chunking (Optimized)
    ENABLE_STREAMING: bool = True
    STREAM_CHUNK_SIZE: int = 1024  # Larger chunks for faster streaming

    # Rate Limiting (Increased)
    MAX_REQUESTS_PER_MINUTE: int = 100  # Higher rate limit

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        extra = "ignore"


try:
    config = Settings()
except Exception:
    config = Settings(_env_file=None)

# Boost Mode Polling Rates (Ultra-Fast)
POLL_RATE = 0.03 if config.VENOM_BOOST else 0.5  # Lightning fast!
WEB_POLL_RATE = 0.02 if config.VENOM_BOOST else 0.1  # Near real-time

if config.VENOM_BOOST:
    try:
        # Try UTF-8 encoding for emojis
        print("=" * 80)
        print("[⚡ VENOM ULTIMATE TURBO MODE ⚡]")
        print(f"  🚀 Cache: {config.CACHE_SIZE} items x {config.CACHE_TTL}s TTL")
        print(f"  🔗 Connection Pool: {config.MAX_CONNECTIONS} connections")
        print(
            f"  ⚙️  Workers: {config.MAX_WORKERS_THREADS} threads | {config.MAX_WORKERS_PROCESSES} processes"
        )
        print(f"  🧠 Memory: {config.MEMORY_WORKING_SIZE} working slots")
        print(f"  ⚡ Poll Rate: {POLL_RATE}s (ULTRA FAST)")
        print(
            f"  🎯 Smart Routing: {'✓ ACTIVE' if config.ENABLE_SMART_ROUTING else '✗ DISABLED'}"
        )
        print(f"  📊 Batch Size: {config.BATCH_SIZE} requests")
        print(f"  🌊 Stream Chunks: {config.STREAM_CHUNK_SIZE} bytes")
        print("=" * 80)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe output for Windows cp1252 consoles
        print("=" * 80)
        print("[* VENOM ULTIMATE TURBO MODE *]")
        print(f"  >> Cache: {config.CACHE_SIZE} items x {config.CACHE_TTL}s TTL")
        print(f"  >> Connection Pool: {config.MAX_CONNECTIONS} connections")
        print(
            f"  >> Workers: {config.MAX_WORKERS_THREADS} threads | {config.MAX_WORKERS_PROCESSES} processes"
        )
        print(f"  >> Memory: {config.MEMORY_WORKING_SIZE} working slots")
        print(f"  >> Poll Rate: {POLL_RATE}s (ULTRA FAST)")
        print(
            f"  >> Smart Routing: {'ACTIVE' if config.ENABLE_SMART_ROUTING else 'DISABLED'}"
        )
        print(f"  >> Batch Size: {config.BATCH_SIZE} requests")
        print(f"  >> Stream Chunks: {config.STREAM_CHUNK_SIZE} bytes")
        print("=" * 80)

# Ensure directories exist
os.makedirs(config.DATA_DIR, exist_ok=True)
os.makedirs(config.MEMORY_DIR, exist_ok=True)
