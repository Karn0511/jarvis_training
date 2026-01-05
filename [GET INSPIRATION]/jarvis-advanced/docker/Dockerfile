# Use Python 3.12 slim image (3.13 not supported by pydantic-core)
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY cli/ ./cli/
COPY backend/ ./backend/
COPY setup.py .

# Create default .env file
RUN echo "# JARVIS AI Configuration\n\
JARVIS_BACKEND_URL=http://127.0.0.1:8574\n\
HOST=0.0.0.0\n\
PORT=8574\n\
DEBUG=true\n\
WORKERS=4\n\
\n\
# Redis\n\
REDIS_URL=redis://redis:6379\n\
CACHE_TTL=300\n\
\n\
# API Keys\n\
OPENAI_API_KEY=\n\
ANTHROPIC_API_KEY=\n\
\n\
# Features\n\
ENABLE_SHELL_EXECUTION=false\n\
ENABLE_QUANTUM=false\n\
USE_LOCAL_LLM=true" > .env

# Install CLI package
RUN pip install -e .

# Create directories
RUN mkdir -p /app/logs /app/data /app/cache

# Expose port
EXPOSE 8574

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8574/api/v1/health || exit 1

# Run the FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8574"]
