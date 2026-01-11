
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import asyncio
import os
from .synapse import synapse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATE_FILE = "data/venom_state.json"

@app.get("/api/status")
async def get_status():
    """REST endpoint for simple polling"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                return json.load(f)
    except:
        pass
    return {"status": "OFFLINE", "vitals": {}}

@app.websocket("/ws/system-stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    Real-time push of system state to Angular
    """
    await websocket.accept()
    last_state = ""
    try:
        while True:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r") as f:
                    current_data = f.read()
                    
                # Push only on change or heartbeat
                if current_data != last_state:
                    try:
                        # Parse verify valid json
                        json_data = json.loads(current_data)
                        await websocket.send_json(json_data)
                        last_state = current_data
                    except:
                        pass
            
            await asyncio.sleep(0.1) # Fast poll local file
    except Exception as e:
        print(f"WebSocket Error: {e}")

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_server()


