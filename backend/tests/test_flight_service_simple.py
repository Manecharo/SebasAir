import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

# Import the functions to test
from src.services.flight_service import (
    get_active_flights,
    get_flight_by_id,
    get_flights_by_date,
    create_flight,
    update_flight,
    delete_flight
)

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
@patch('src.services.flight_service.Flight')
def test_create_flight(mock_flight_class, mock_db):
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
    
    # Create a mock instance for the Flight class
    mock_flight_instance = MagicMock()
    mock_flight_class.return_value = mock_flight_instance
    
    # Call the function
    result = create_flight(mock_db, new_flight_data)
    
    # Assertions
    mock_flight_class.assert_called_once_with(**new_flight_data)
    mock_db.add.assert_called_once_with(mock_flight_instance)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_flight_instance)
    assert result == mock_flight_instance

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