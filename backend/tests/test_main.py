import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from datetime import datetime

from src.main import app
from src.models.flight import Flight

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Welcome to the Air Ambulance Flight Tracker API" in response.json()["message"]

@patch("src.routers.flights.get_flights")
def test_flights_endpoint(mock_get_flights, client, mock_db):
    # Setup mock
    mock_flight = MagicMock(spec=Flight)
    mock_flight.id = 1
    mock_flight.flight_id = "ABC123"
    mock_flight.tail_number = "N12345"
    mock_flight.status = "ACTIVE"
    mock_flight.departure_time = datetime.now()
    mock_flight.arrival_time = None
    mock_flight.current_position_lat = 40.7128
    mock_flight.current_position_lon = -74.0060
    mock_flight.altitude = 30000
    mock_flight.speed = 500
    mock_flight.heading = 90
    
    mock_get_flights.return_value = [mock_flight]
    
    response = client.get("/api/flights")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "flights" in response.json()

@patch("src.routers.flights.get_active_flights")
def test_active_flights_endpoint(mock_get_active_flights, client, mock_db):
    # Setup mock
    mock_flight = MagicMock(spec=Flight)
    mock_flight.id = 1
    mock_flight.flight_id = "ABC123"
    mock_flight.tail_number = "N12345"
    mock_flight.status = "ACTIVE"
    mock_flight.departure_time = datetime.now()
    mock_flight.arrival_time = None
    mock_flight.current_position_lat = 40.7128
    mock_flight.current_position_lon = -74.0060
    mock_flight.altitude = 30000
    mock_flight.speed = 500
    mock_flight.heading = 90
    
    mock_get_active_flights.return_value = [mock_flight]
    
    response = client.get("/api/flights/active")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "flights" in response.json()

def test_websocket_endpoint_exists(client):
    # We can't test the WebSocket connection directly with TestClient,
    # but we can check that the endpoint exists
    response = client.get("/docs")
    assert response.status_code == 200
    assert "ws/flights" in response.text
