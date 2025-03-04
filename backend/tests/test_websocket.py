import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import json
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from datetime import datetime

from src.main import app
from src.websockets.flight_socket import FlightTrackingManager, flight_manager

client = TestClient(app)

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

@pytest.fixture
def mock_websocket():
    """Create a mock WebSocket for testing."""
    mock_ws = MagicMock(spec=WebSocket)
    mock_ws.accept = AsyncMock()
    mock_ws.send_json = AsyncMock()
    mock_ws.receive_text = AsyncMock(return_value="get_flights")
    return mock_ws

@pytest.mark.asyncio
async def test_flight_manager_connect(mock_websocket):
    """Test that a WebSocket connection can be established."""
    # Create a new manager for testing
    manager = FlightTrackingManager()
    
    # Connect the mock WebSocket
    await manager.connect(mock_websocket)
    
    # Assert that accept was called
    mock_websocket.accept.assert_called_once()
    
    # Assert that the connection was added to active_connections
    assert mock_websocket in manager.active_connections

@pytest.mark.asyncio
async def test_flight_manager_disconnect(mock_websocket):
    """Test that a WebSocket connection can be disconnected."""
    # Create a new manager for testing
    manager = FlightTrackingManager()
    
    # Add the mock WebSocket to active_connections
    manager.active_connections.append(mock_websocket)
    
    # Disconnect the mock WebSocket
    manager.disconnect(mock_websocket)
    
    # Assert that the connection was removed from active_connections
    assert mock_websocket not in manager.active_connections

@pytest.mark.asyncio
async def test_flight_manager_broadcast(mock_websocket):
    """Test that data can be broadcast to all connected clients."""
    # Create a new manager for testing
    manager = FlightTrackingManager()
    
    # Add the mock WebSocket to active_connections
    manager.active_connections.append(mock_websocket)
    
    # Create test data
    test_data = {
        "flights": [
            {
                "id": 1,
                "flight_id": "ABC123",
                "status": "ACTIVE"
            }
        ]
    }
    
    # Broadcast the test data
    await manager.broadcast(test_data)
    
    # Assert that send_json was called with the test data
    mock_websocket.send_json.assert_called_once()
    
    # Check that the timestamp was added
    call_args = mock_websocket.send_json.call_args[0][0]
    assert "timestamp" in call_args
    assert "flights" in call_args

@pytest.mark.asyncio
async def test_flight_manager_broadcast_with_exception(mock_websocket):
    """Test that exceptions during broadcast are handled properly."""
    # Create a new manager for testing
    manager = FlightTrackingManager()
    
    # Create a mock WebSocket that raises an exception
    mock_ws_exception = MagicMock(spec=WebSocket)
    mock_ws_exception.send_json = AsyncMock(side_effect=Exception("Test exception"))
    
    # Add both WebSockets to active_connections
    manager.active_connections.append(mock_websocket)
    manager.active_connections.append(mock_ws_exception)
    
    # Create test data
    test_data = {
        "flights": [
            {
                "id": 1,
                "flight_id": "ABC123",
                "status": "ACTIVE"
            }
        ]
    }
    
    # Broadcast the test data
    await manager.broadcast(test_data)
    
    # Assert that the exception WebSocket was removed
    assert mock_ws_exception not in manager.active_connections
    
    # Assert that the good WebSocket is still there
    assert mock_websocket in manager.active_connections
    
    # Assert that send_json was called on the good WebSocket
    mock_websocket.send_json.assert_called_once()

@pytest.mark.asyncio
async def test_flight_manager_connect_with_last_data(mock_websocket):
    """Test that a new connection receives the last flight data."""
    # Create a new manager for testing
    manager = FlightTrackingManager()
    
    # Set last_flight_data
    manager.last_flight_data = {
        "flights": [
            {
                "id": 1,
                "flight_id": "ABC123",
                "status": "ACTIVE"
            }
        ]
    }
    
    # Connect the mock WebSocket
    await manager.connect(mock_websocket)
    
    # Assert that send_json was called with the last flight data
    mock_websocket.send_json.assert_called_once_with(manager.last_flight_data)

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