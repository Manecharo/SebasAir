import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime, timedelta

from src.services.flight_update_service import update_flight_position
from src.models.flight import Flight

@pytest.fixture
def mock_flight():
    """Create a mock flight for testing."""
    return Flight(
        id=1,
        flight_id="ABC123",
        tail_number="N12345",
        status="ACTIVE",
        departure_time=datetime.now() - timedelta(hours=1),
        arrival_time=None,
        current_position_lat=40.7128,
        current_position_lon=-74.0060,
        altitude=30000,
        speed=500,
        heading=90,
        updated_at=datetime.now() - timedelta(seconds=10)
    )

@pytest.fixture
def mock_db():
    """Create a mock database session for testing."""
    return MagicMock()

def test_update_flight_position_east(mock_flight, mock_db):
    """Test updating a flight's position when heading east (90 degrees)."""
    # Set heading to east
    mock_flight.heading = 90
    
    # Store original position
    original_lat = mock_flight.current_position_lat
    original_lon = mock_flight.current_position_lon
    
    # Update position
    update_flight_position(mock_flight, mock_db)
    
    # Assert that latitude didn't change much (heading east)
    assert abs(mock_flight.current_position_lat - original_lat) < 0.1
    
    # Assert that longitude increased (heading east)
    assert mock_flight.current_position_lon > original_lon

def test_update_flight_position_north(mock_flight, mock_db):
    """Test updating a flight's position when heading north (0 degrees)."""
    # Set heading to north
    mock_flight.heading = 0
    
    # Store original position
    original_lat = mock_flight.current_position_lat
    original_lon = mock_flight.current_position_lon
    
    # Update position
    update_flight_position(mock_flight, mock_db)
    
    # Assert that latitude increased (heading north)
    assert mock_flight.current_position_lat > original_lat
    
    # Assert that longitude didn't change much (heading north)
    assert abs(mock_flight.current_position_lon - original_lon) < 0.1

def test_update_flight_position_west(mock_flight, mock_db):
    """Test updating a flight's position when heading west (270 degrees)."""
    # Set heading to west
    mock_flight.heading = 270
    
    # Store original position
    original_lat = mock_flight.current_position_lat
    original_lon = mock_flight.current_position_lon
    
    # Update position
    update_flight_position(mock_flight, mock_db)
    
    # Assert that latitude didn't change much (heading west)
    assert abs(mock_flight.current_position_lat - original_lat) < 0.1
    
    # Assert that longitude decreased (heading west)
    assert mock_flight.current_position_lon < original_lon

def test_update_flight_position_south(mock_flight, mock_db):
    """Test updating a flight's position when heading south (180 degrees)."""
    # Set heading to south
    mock_flight.heading = 180
    
    # Store original position
    original_lat = mock_flight.current_position_lat
    original_lon = mock_flight.current_position_lon
    
    # Update position
    update_flight_position(mock_flight, mock_db)
    
    # Assert that latitude decreased (heading south)
    assert mock_flight.current_position_lat < original_lat
    
    # Assert that longitude didn't change much (heading south)
    assert abs(mock_flight.current_position_lon - original_lon) < 0.1

def test_update_flight_position_northeast(mock_flight, mock_db):
    """Test updating a flight's position when heading northeast (45 degrees)."""
    # Set heading to northeast
    mock_flight.heading = 45
    
    # Store original position
    original_lat = mock_flight.current_position_lat
    original_lon = mock_flight.current_position_lon
    
    # Update position
    update_flight_position(mock_flight, mock_db)
    
    # Assert that latitude increased (heading north component)
    assert mock_flight.current_position_lat > original_lat
    
    # Assert that longitude increased (heading east component)
    assert mock_flight.current_position_lon > original_lon

def test_update_flight_position_no_coordinates(mock_flight, mock_db):
    """Test that nothing happens when the flight has no coordinates."""
    # Set coordinates to None
    mock_flight.current_position_lat = None
    mock_flight.current_position_lon = None
    
    # Update position
    update_flight_position(mock_flight, mock_db)
    
    # Assert that coordinates are still None
    assert mock_flight.current_position_lat is None
    assert mock_flight.current_position_lon is None

def test_update_flight_position_altitude_and_speed_changes(mock_flight, mock_db):
    """Test that altitude and speed are updated with some randomness."""
    # Store original values
    original_altitude = mock_flight.altitude
    original_speed = mock_flight.speed
    
    # Update position
    update_flight_position(mock_flight, mock_db)
    
    # Assert that altitude changed
    assert mock_flight.altitude != original_altitude
    
    # Assert that speed changed
    assert mock_flight.speed != original_speed
    
    # Assert that altitude is within bounds
    assert 20000 <= mock_flight.altitude <= 40000
    
    # Assert that speed is within bounds
    assert 400 <= mock_flight.speed <= 600

def test_update_flight_position_updated_at(mock_flight, mock_db):
    """Test that the updated_at timestamp is updated."""
    # Store original timestamp
    original_updated_at = mock_flight.updated_at
    
    # Update position
    update_flight_position(mock_flight, mock_db)
    
    # Assert that updated_at was updated
    assert mock_flight.updated_at > original_updated_at 