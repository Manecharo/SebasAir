from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Any
import json
import asyncio
from datetime import datetime

# Class to manage WebSocket connections
class FlightTrackingManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.last_flight_data: Dict[str, Any] = {}
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        # Send the current flight data to the new connection
        if self.last_flight_data:
            await websocket.send_json(self.last_flight_data)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, data: Dict[str, Any]):
        # Update the last flight data
        self.last_flight_data = data
        
        # Add timestamp
        data["timestamp"] = datetime.now().isoformat()
        
        # Broadcast to all connected clients
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception:
                # Remove any connections that fail
                self.active_connections.remove(connection)

# Create a global instance of the manager
flight_manager = FlightTrackingManager() 