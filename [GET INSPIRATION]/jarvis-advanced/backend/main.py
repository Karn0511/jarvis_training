"""Clean backend entrypoint with local-only LLM, streaming, metrics."""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import json
import re
import subprocess
import time
from collections import deque
from datetime import datetime

from core.config import settings
from core.cache import cache
from core.llm_router import llm_router
from api.websocket_handler import ConnectionManager

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Advanced AI Coding Assistant (Local Mode)",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ws_manager = ConnectionManager()
request_times = deque(maxlen=1000)
start_time = time.time()

class ChatRequest(BaseModel):
    message: str
    context: Optional[List[dict]] = None
    stream: bool = False

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str
    filename: Optional[str] = None

class ExecuteRequest(BaseModel):
    command: str
    timeout: int = 30

@app.on_event("startup")
async def startup_event():
    await cache.initialize()
    print(f"🚀 Starting {settings.APP_NAME} v{settings.VERSION}")

@app.on_event("shutdown")
async def shutdown_event():
    print("👋 Shutting down gracefully...")

@app.middleware("http")
async def record_timing(request, call_next):
    started = time.time()
    response = await call_next(request)
    request_times.append(started)
    return response

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "online",
        "local_only": True,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "cache": "redis" if cache.redis else "memory",
        "recent_requests": len(request_times),
        "uptime_seconds": int(time.time() - start_time)
    }

def _avg_rps():
    if not request_times:
        return 0
    window = time.time() - request_times[0]
    return round(len(request_times) / window, 2) if window > 0 else 0

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if request.stream:
        return StreamingResponse(stream_response(request.message), media_type="text/event-stream")
    response = await llm_router.query(prompt=request.message, system_prompt="You are Jarvis, a helpful local coding assistant.")
    return {
        "answer": response['answer'],
        "model": response['model'],
        "cached": response.get('cached', False),
        "timestamp": datetime.utcnow().isoformat()
    }

async def stream_response(message: str, chunk_size: int = 48):
    response = await llm_router.query(message)
    text = response['answer']
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        done = i + chunk_size >= len(text)
        yield f"data: {json.dumps({'delta': chunk, 'done': done})}\n\n"

@app.post("/api/analyze")
async def analyze_code(request: CodeAnalysisRequest):
    code = request.code
    language = request.language
    lines = code.split('\n')
    line_count = len(lines)
    prompt = f"""Analyze this {language} code and provide concise JSON with keys: quality (0-10), complexity (0-10), issues_count, summary, suggestions (array).\nLines: {line_count}\nCode:\n{code}"""
    response = await llm_router.query(prompt)
    try:
        json_match = re.search(r'\{.*\}', response['answer'], re.DOTALL)
        analysis = json.loads(json_match.group()) if json_match else {}
    except Exception:
        analysis = {}
    # Defaults
    analysis.setdefault('quality', 7)
    analysis.setdefault('complexity', 5)
    analysis.setdefault('issues_count', 0)
    analysis.setdefault('summary', response['answer'][:400])
    return {**analysis, "language": language, "lines": line_count, "model": response['model']}

@app.post("/api/refactor")
async def refactor_code(request: CodeAnalysisRequest):
    prompt = f"Refactor this {request.language} code for readability and performance. Return only code.\n{request.code}"
    response = await llm_router.query(prompt)
    return {"refactored": response['answer'], "model": response['model']}

@app.post("/api/execute")
async def execute_command(request: ExecuteRequest):
    if not settings.ENABLE_SHELL_EXECUTION:
        raise HTTPException(status_code=403, detail="Shell execution disabled")
    try:
        result = subprocess.run(request.command, shell=True, capture_output=True, text=True, timeout=request.timeout)
        return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get('type') == 'chat':
                response = await llm_router.query(data['message'])
                await websocket.send_json({"type": "chat_response", "message": response['answer'], "model": response['model']})
            elif data.get('type') == 'ping':
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

@app.get("/api/stats")
async def get_stats():
    return {
        "active_connections": len(ws_manager.active_connections),
        "cache_type": "redis" if cache.redis else "memory",
        "uptime_seconds": int(time.time() - start_time),
        "recent_requests": len(request_times),
        "avg_rps": _avg_rps()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
