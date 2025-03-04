import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import json
from datetime import datetime

# Mock WebSocket class for testing
class MockWebSocket:
    def __init__(self):
        self.sent_messages = []
        self.client_state = {}
        
    async def accept(self):
        return None
        
    async def send_json(self, data):
        self.sent_messages.append(data)
        
    async def receive_json(self):
        return {"type": "test", "data": "test_data"}

# Mock FlightTrackingManager class
class MockFlightTrackingManager:
    def __init__(self):
        self.active_connections = []
        
    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            
    async def broadcast(self, data):
        for connection in self.active_connections:
            await connection.send_json({
                "timestamp": datetime.now().isoformat(),
                **data
            })

# Test WebSocket connection
@pytest.mark.asyncio
async def test_websocket_connect():
    # Create a mock WebSocket
    websocket = MockWebSocket()
    
    # Create a mock manager
    manager = MockFlightTrackingManager()
    
    # Connect the WebSocket
    await manager.connect(websocket)
    
    # Assert that the connection was added to active_connections
    assert websocket in manager.active_connections

# Test WebSocket disconnection
@pytest.mark.asyncio
async def test_websocket_disconnect():
    # Create a mock WebSocket
    websocket = MockWebSocket()
    
    # Create a mock manager
    manager = MockFlightTrackingManager()
    
    # Add the WebSocket to active_connections
    manager.active_connections.append(websocket)
    
    # Disconnect the WebSocket
    manager.disconnect(websocket)
    
    # Assert that the connection was removed from active_connections
    assert websocket not in manager.active_connections

# Test WebSocket broadcast
@pytest.mark.asyncio
async def test_websocket_broadcast():
    # Create a mock WebSocket
    websocket = MockWebSocket()
    
    # Create a mock manager
    manager = MockFlightTrackingManager()
    
    # Add the WebSocket to active_connections
    manager.active_connections.append(websocket)
    
    # Broadcast a message
    test_data = {"message": "test message"}
    await manager.broadcast(test_data)
    
    # Assert that the message was sent
    assert len(websocket.sent_messages) == 1
    assert "timestamp" in websocket.sent_messages[0]
    assert websocket.sent_messages[0]["message"] == "test message"

# Test WebSocket receive
@pytest.mark.asyncio
async def test_websocket_receive():
    # Create a mock WebSocket
    websocket = MockWebSocket()
    
    # Receive a message
    received = await websocket.receive_json()
    
    # Assert that the message was received
    assert received == {"type": "test", "data": "test_data"} 