"""
Advanced Configuration with Environment Management
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional
import os

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Jarvis AI"
    VERSION: str = "2.0.0"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8574
    WORKERS: int = 4

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Redis Cache (optional - falls back to memory)
    REDIS_URL: Optional[str] = None
    CACHE_TTL: int = 300

    # AI Models
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None

    # Local Models
    USE_LOCAL_LLM: bool = True
    LOCAL_MODEL_PATH: str = "./models/llama"

    # Quantum
    ENABLE_QUANTUM: bool = False
    QUANTUM_BACKEND: str = "pennylane"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Features
    MAX_FILE_SIZE: int = 10_000_000  # 10MB
    MAX_CONTEXT_LENGTH: int = 8000
    ENABLE_SHELL_EXECUTION: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
