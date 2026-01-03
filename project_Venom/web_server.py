from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
import json
import asyncio
import os
import sys
import aiofiles
import mimetypes
from pydantic import BaseModel

# Force MIME type registration for slim Docker images
mimetypes.init()
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")

# Ensure core modules are found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import configuration
try:
    from ai_core.core.synapse import synapse
    from ai_core.core.config import WEB_POLL_RATE

    HAS_CORE = True
except ImportError:
    HAS_CORE = False
    WEB_POLL_RATE = 0.5
    print("WARNING: Core modules not found. Running in skeleton mode.")

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATE_FILE = "storage/venom_state.json"


class CommandRequest(BaseModel):
    text: str


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker/K8s probes."""
    return {"status": "healthy", "service": "venom-api"}


@app.post("/api/command")
async def receive_command(cmd: CommandRequest):
    """Endpoint for Angular to push commands."""
    print(f"WEB COMMAND RECEIVED: {cmd.text}")
    if HAS_CORE:
        synapse.monitor_input = True
        synapse.push_input(cmd.text)

    # Immediate acknowledgement
    return {
        "status": "processing",
        "message": "Command received by Venom Neural Core",
        "input": cmd.text,
    }


@app.get("/api/state")
async def get_system_state():
    """Get current system state."""
    if os.path.exists(STATE_FILE):
        try:
            async with aiofiles.open(STATE_FILE, "r", encoding="utf-8") as f:
                content = await f.read()
                return json.loads(content)
        except Exception:
            pass

    # Fallback state
    return {
        "status": "LISTENING",
        "detail": "Neural core ready",
        "vitals": {"cpu_percent": 35, "ram_percent": 45, "neural_activity": 50},
    }


@app.websocket("/ws/system-stream")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time system state streaming."""
    await websocket.accept()
    last_state = ""
    try:
        while True:
            # Poll file state (simple IPC)
            if os.path.exists(STATE_FILE):
                try:
                    async with aiofiles.open(STATE_FILE, "r", encoding="utf-8") as f:
                        current_data = await f.read()

                    if current_data != last_state:
                        # Verify JSON before sending
                        json.loads(current_data)
                        await websocket.send_text(current_data)
                        last_state = current_data
                except Exception:
                    pass
            await asyncio.sleep(WEB_POLL_RATE)
    except Exception as e:
        print(f"WebSocket Disconnected: {e}")


# Serve Angular Frontend (Dynamic Detection)
FRONTEND_SEARCH_PATHS = [
    "frontend/dist/venom-dashboard/browser",
    "frontend/dist/venom-dashboard",
    "dashboard/dist/browser",
    "dist/browser",
]

FRONTEND_PATH = None
for path in FRONTEND_SEARCH_PATHS:
    if os.path.exists(path) and os.path.isdir(path):
        FRONTEND_PATH = os.path.abspath(path)
        break

if FRONTEND_PATH:
    print(f"WEB HUD: Found UI at {FRONTEND_PATH}")

    # Define route to serve specific files first
    @app.get("/{path:path}")
    async def serve_frontend(request: Request, path: str):
        # Prevent API/WS from being swallowed
        if path.startswith("api") or path.startswith("ws"):
            return JSONResponse(status_code=404, content={"error": "Not Found"})

        full_path = os.path.join(FRONTEND_PATH, path)

        # If the file exists, serve it
        if os.path.isfile(full_path):
            # Check extension to set MIME type explicitly if needed
            ext = os.path.splitext(full_path)[1].lower()
            mime_type = mimetypes.guess_type(full_path)[0] or "application/octet-stream"
            return FileResponse(full_path, media_type=mime_type)

        # If it's a folder or nothing, or a client-side route, serve index.html
        index_file = os.path.join(FRONTEND_PATH, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)

        return JSONResponse(
            status_code=404, content={"error": "Interface files missing"}
        )

else:
    print("Warning: Frontend build not found. Running in API-only mode.")


if __name__ == "__main__":
    print("VENOM WEB SERVER STARTING ON PORT 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
