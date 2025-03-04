import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.services.flight_service import (
    get_flights,
    get_flight_by_id,
    create_flight,
    update_flight,
    get_active_flights,
    get_flights_by_date,
    delete_flight
)
from src.models.flight import Flight
from src.services.flight_service import FlightService

# Mock data
mock_flight_data = {
    "flight_id": "ABC123",
    "tail_number": "N12345",
    "status": "ACTIVE",
    "departure_time": datetime.now() - timedelta(hours=1),
    "current_position_lat": 40.7128,
    "current_position_lon": -74.0060,
    "altitude": 30000,
    "speed": 500,
    "heading": 90
}

mock_flight = Flight(
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
    heading=90
)

mock_completed_flight = Flight(
    id=2,
    flight_id="DEF456",
    tail_number="N67890",
    status="COMPLETED",
    departure_time=datetime.now() - timedelta(hours=3),
    arrival_time=datetime.now() - timedelta(hours=1),
    current_position_lat=41.8781,
    current_position_lon=-87.6298,
    altitude=0,
    speed=0,
    heading=0
)

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_get_flights(mock_db):
    # Setup
    mock_db.query.return_value.all.return_value = [mock_flight, mock_completed_flight]
    
    # Execute
    result = get_flights(mock_db)
    
    # Assert
    assert len(result) == 2
    assert result[0].flight_id == "ABC123"
    assert result[1].flight_id == "DEF456"

def test_get_flight_by_id(mock_db):
    # Setup
    mock_db.query.return_value.filter.return_value.first.return_value = mock_flight
    
    # Execute
    result = get_flight_by_id(mock_db, 1)
    
    # Assert
    assert result.id == 1
    assert result.flight_id == "ABC123"
    
    # Test not found
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = get_flight_by_id(mock_db, 999)
    assert result is None

def test_create_flight(mock_db):
    # Setup
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    # Execute
    result = create_flight(mock_db, mock_flight_data)
    
    # Assert
    assert result.flight_id == "ABC123"
    assert result.tail_number == "N12345"
    assert result.status == "ACTIVE"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_update_flight(mock_db):
    # Setup
    mock_db.query.return_value.filter.return_value.first.return_value = mock_flight
    mock_db.commit.return_value = None
    
    update_data = {
        "status": "DELAYED",
        "altitude": 35000,
        "speed": 450
    }
    
    # Execute
    result = update_flight(mock_db, 1, update_data)
    
    # Assert
    assert result.status == "DELAYED"
    assert result.altitude == 35000
    assert result.speed == 450
    mock_db.commit.assert_called_once()
    
    # Test not found
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = update_flight(mock_db, 999, update_data)
    assert result is None

def test_get_active_flights(mock_db):
    # Setup
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_flight]
    
    # Execute
    result = get_active_flights(mock_db)
    
    # Assert
    assert len(result) == 1
    assert result[0].flight_id == "ABC123"
    assert result[0].status == "ACTIVE"
    
    # Test no active flights
    mock_db.query.return_value.filter.return_value.all.return_value = []
    result = get_active_flights(mock_db)
    assert len(result) == 0

# Test data
mock_flight_data = [
    {
        "id": 1,
        "flight_number": "COL123",
        "origin": "BOG",
        "destination": "MDE",
        "scheduled_departure": datetime.now(),
        "scheduled_arrival": datetime.now() + timedelta(hours=1),
        "status": "active",
        "aircraft_id": 1,
        "created_at": datetime.now() - timedelta(days=1),
        "updated_at": datetime.now()
    },
    {
        "id": 2,
        "flight_number": "COL456",
        "origin": "MDE",
        "destination": "BOG",
        "scheduled_departure": datetime.now() + timedelta(hours=2),
        "scheduled_arrival": datetime.now() + timedelta(hours=3),
        "status": "scheduled",
        "aircraft_id": 2,
        "created_at": datetime.now() - timedelta(days=1),
        "updated_at": datetime.now()
    }
]

# Test getting all flights
def test_get_all_flights(mock_db):
    # Setup mock
    mock_db.query.return_value.all.return_value = mock_flight_data
    
    # Create service instance
    service = FlightService(mock_db)
    
    # Call the method
    result = service.get_all_flights()
    
    # Assertions
    assert result == mock_flight_data
    mock_db.query.assert_called_once()
    mock_db.query.return_value.all.assert_called_once()

# Test getting active flights
def test_get_active_flights(mock_db):
    # Setup mock
    active_flights = [flight for flight in mock_flight_data if flight["status"] == "active"]
    mock_db.query.return_value.filter.return_value.all.return_value = active_flights
    
    # Call the function
    result = get_active_flights(mock_db)
    
    # Assertions
    assert result == active_flights
    mock_db.query.assert_called_once()
    mock_db.query.return_value.filter.assert_called_once()
    mock_db.query.return_value.filter.return_value.all.assert_called_once()

# Test getting a flight by ID
def test_get_flight_by_id(mock_db):
    # Setup mock
    flight_id = 1
    mock_flight = mock_flight_data[0]
    mock_db.query.return_value.filter.return_value.first.return_value = mock_flight
    
    # Call the function
    result = get_flight_by_id(mock_db, flight_id)
    
    # Assertions
    assert result == mock_flight
    mock_db.query.assert_called_once()
    mock_db.query.return_value.filter.assert_called_once()
    mock_db.query.return_value.filter.return_value.first.assert_called_once()

# Test getting flights by date
def test_get_flights_by_date(mock_db):
    # Setup mock
    test_date = datetime.now().date()
    mock_db.query.return_value.filter.return_value.all.return_value = mock_flight_data
    
    # Call the function
    result = get_flights_by_date(mock_db, test_date)
    
    # Assertions
    assert result == mock_flight_data
    mock_db.query.assert_called_once()
    mock_db.query.return_value.filter.assert_called_once()
    mock_db.query.return_value.filter.return_value.all.assert_called_once()

# Test creating a flight
def test_create_flight(mock_db):
    # Setup mock
    new_flight_data = {
        "flight_number": "COL789",
        "origin": "BOG",
        "destination": "CTG",
        "scheduled_departure": datetime.now() + timedelta(days=1),
        "scheduled_arrival": datetime.now() + timedelta(days=1, hours=1),
        "status": "scheduled",
        "aircraft_id": 3
    }
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
    
    # Call the function
    result = create_flight(mock_db, new_flight_data)
    
    # Assertions
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

# Test updating a flight
def test_update_flight(mock_db):
    # Setup mock
    flight_id = 1
    update_data = {"status": "delayed"}
    mock_flight = MagicMock()
    
    # Mock the get_flight_by_id function
    with patch('src.services.flight_service.get_flight_by_id') as mock_get_flight:
        mock_get_flight.return_value = mock_flight
        
        # Call the function
        result = update_flight(mock_db, flight_id, update_data)
        
        # Assertions
        assert result == mock_flight
        mock_get_flight.assert_called_once_with(mock_db, flight_id)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
# Test deleting a flight
def test_delete_flight(mock_db):
    # Setup mock
    flight_id = 1
    mock_flight = MagicMock()
    
    # Mock the get_flight_by_id function
    with patch('src.services.flight_service.get_flight_by_id') as mock_get_flight:
        mock_get_flight.return_value = mock_flight
        
        # Call the function
        result = delete_flight(mock_db, flight_id)
        
        # Assertions
        assert result is True
        mock_get_flight.assert_called_once_with(mock_db, flight_id)
        mock_db.delete.assert_called_once_with(mock_flight)
        mock_db.commit.assert_called_once() 