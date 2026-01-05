"""
WebSocket Connection Manager
"""
from fastapi import WebSocket
from typing import List
import json

class ConnectionManager:
    """Manages WebSocket connections"""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept new connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ Client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove connection"""
        self.active_connections.remove(websocket)
        print(f"❌ Client disconnected. Total: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send to specific client"""
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        """Broadcast to all clients"""
        for connection in self.active_connections:
            await connection.send_json(message)
