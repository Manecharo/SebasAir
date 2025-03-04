import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from ..src.services.flight_data_service import FlightDataService
from ..src.services.flightradar24_client import FlightRadar24Client

@pytest.fixture
def mock_fr24_client():
    return Mock(spec=FlightRadar24Client)

@pytest.fixture
def flight_service(mock_fr24_client):
    return FlightDataService(fr24_client=mock_fr24_client)

def test_get_live_flights_success(flight_service, mock_fr24_client):
    """Test successful retrieval of live flights."""
    mock_raw_data = {
        'flights': [
            {
                'id': 'ABC123',
                'callsign': 'TEST123',
                'registration': 'N123AB',
                'aircraft': {'type': 'B738'},
                'latitude': 40.7128,
                'longitude': -74.0060,
                'altitude': 30000,
                'speed': 500,
                'heading': 90,
                'status': 'active',
                'departure': {'code': 'KJFK'},
                'arrival': {'code': 'KLAX'},
                'airline': {'name': 'Test Airlines'}
            }
        ]
    }
    
    mock_fr24_client.get_live_flights.return_value = mock_raw_data
    
    result = flight_service.get_live_flights(bounds="50.682,46.218,14.422,22.243")
    
    assert len(result) == 1
    flight = result[0]
    assert flight['flight_id'] == 'ABC123'
    assert flight['callsign'] == 'TEST123'
    assert flight['registration'] == 'N123AB'
    assert flight['aircraft_type'] == 'B738'
    assert flight['latitude'] == 40.7128
    assert flight['longitude'] == -74.0060
    assert flight['altitude'] == 30000
    assert flight['speed'] == 500
    assert flight['heading'] == 90
    assert flight['status'] == 'active'
    assert flight['departure_airport'] == 'KJFK'
    assert flight['arrival_airport'] == 'KLAX'
    assert flight['airline'] == 'Test Airlines'
    assert 'last_updated' in flight

def test_get_live_flights_error(flight_service, mock_fr24_client):
    """Test error handling when fetching live flights."""
    mock_fr24_client.get_live_flights.side_effect = Exception("API Error")
    
    result = flight_service.get_live_flights()
    
    assert result == []

def test_get_flight_details_success(flight_service, mock_fr24_client):
    """Test successful retrieval of flight details."""
    mock_flight_details = {
        'flight': {
            'id': 'ABC123',
            'status': 'active'
        }
    }
    
    mock_fr24_client.get_flight_details.return_value = mock_flight_details
    
    result = flight_service.get_flight_details('ABC123')
    
    assert result == mock_flight_details
    mock_fr24_client.get_flight_details.assert_called_once_with('ABC123')

def test_get_flight_details_error(flight_service, mock_fr24_client):
    """Test error handling when fetching flight details."""
    mock_fr24_client.get_flight_details.side_effect = Exception("API Error")
    
    result = flight_service.get_flight_details('ABC123')
    
    assert result is None

def test_get_historical_flight_data_success(flight_service, mock_fr24_client):
    """Test successful retrieval of historical flight data."""
    mock_historical_data = {
        'flight': {
            'id': 'ABC123',
            'date': '2024-03-01'
        }
    }
    
    mock_fr24_client.get_historical_flight.return_value = mock_historical_data
    date = datetime(2024, 3, 1)
    
    result = flight_service.get_historical_flight_data('ABC123', date)
    
    assert result == mock_historical_data
    mock_fr24_client.get_historical_flight.assert_called_once_with('ABC123', date)

def test_get_historical_flight_data_error(flight_service, mock_fr24_client):
    """Test error handling when fetching historical flight data."""
    mock_fr24_client.get_historical_flight.side_effect = Exception("API Error")
    date = datetime(2024, 3, 1)
    
    result = flight_service.get_historical_flight_data('ABC123', date)
    
    assert result is None

def test_process_live_flights_handles_missing_data(flight_service):
    """Test processing of live flights with missing data."""
    raw_data = {
        'flights': [
            {
                'id': 'ABC123',
                # Missing most fields
            }
        ]
    }
    
    result = flight_service._process_live_flights(raw_data)
    
    assert len(result) == 1
    flight = result[0]
    assert flight['flight_id'] == 'ABC123'
    assert flight['callsign'] is None
    assert flight['registration'] is None
    assert flight['aircraft_type'] is None
    assert 'last_updated' in flight

def test_process_live_flights_handles_empty_data(flight_service):
    """Test processing of empty flight data."""
    raw_data = {'flights': []}
    
    result = flight_service._process_live_flights(raw_data)
    
    assert result == []

def test_process_live_flights_handles_invalid_data(flight_service):
    """Test processing of invalid flight data."""
    raw_data = {'invalid_key': []}
    
    result = flight_service._process_live_flights(raw_data)
    
    assert result == [] 