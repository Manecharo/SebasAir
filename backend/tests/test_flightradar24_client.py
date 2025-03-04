import pytest
import responses
from datetime import datetime
from urllib.parse import quote
from src.services.flightradar24_client import FlightRadar24Client

@pytest.fixture
def fr24_client():
    """Create a FlightRadar24Client instance for testing."""
    return FlightRadar24Client('test_token')

@pytest.fixture
def mock_live_flights_response():
    """Mock response data for live flights."""
    return {
        'data': [
            {
                'id': 'ABC123',
                'callsign': 'TEST123',
                'registration': 'N123AB',
                'aircraft': {'type': 'B738'},
                'latitude': 40.7128,
                'longitude': -74.0060,
                'altitude': 35000,
                'speed': 450,
                'heading': 90,
                'status': 'EN_ROUTE',
                'departure': {'code': 'JFK'},
                'arrival': {'code': 'LAX'},
                'airline': {'name': 'Test Airlines'}
            }
        ]
    }

@responses.activate
def test_get_live_flights(fr24_client, mock_live_flights_response):
    """Test getting live flights."""
    # Mock the API response
    responses.add(
        responses.GET,
        'https://fr24api.flightradar24.com/api/live/flight-positions/light',
        json=mock_live_flights_response,
        status=200
    )

    # Make the request
    flights = fr24_client.get_live_flights()

    # Verify the response
    assert len(flights) == 1
    flight = flights[0]
    assert flight['flight_id'] == 'ABC123'
    assert flight['callsign'] == 'TEST123'
    assert flight['registration'] == 'N123AB'
    assert flight['aircraft_type'] == 'B738'
    assert flight['latitude'] == 40.7128
    assert flight['longitude'] == -74.0060
    assert flight['altitude'] == 35000
    assert flight['speed'] == 450
    assert flight['heading'] == 90
    assert flight['status'] == 'EN_ROUTE'
    assert flight['departure_airport'] == 'JFK'
    assert flight['arrival_airport'] == 'LAX'
    assert flight['airline'] == 'Test Airlines'

@responses.activate
def test_get_live_flights_with_bounds(fr24_client, mock_live_flights_response):
    """Test getting live flights with bounds parameter."""
    # Mock the API response
    responses.add(
        responses.GET,
        'https://fr24api.flightradar24.com/api/live/flight-positions/light',
        json=mock_live_flights_response,
        status=200
    )

    # Make the request with bounds
    bounds = '50.682,46.218,14.422,22.243'
    flights = fr24_client.get_live_flights(bounds)

    # Verify the request was made with bounds parameter
    assert len(responses.calls) == 1
    request_url = responses.calls[0].request.url
    encoded_bounds = quote(bounds)
    assert f'bounds={encoded_bounds}' in request_url

@responses.activate
def test_get_live_flights_error_handling(fr24_client):
    """Test error handling when getting live flights."""
    # Mock an error response
    responses.add(
        responses.GET,
        'https://fr24api.flightradar24.com/api/live/flight-positions/light',
        status=500
    )

    # Make the request
    flights = fr24_client.get_live_flights()

    # Verify empty list is returned on error
    assert flights == []

@responses.activate
def test_get_flight_details(fr24_client):
    """Test getting flight details."""
    flight_id = 'ABC123'
    mock_response = {
        'data': {
            'id': flight_id,
            'callsign': 'TEST123',
            'status': 'EN_ROUTE'
        }
    }

    # Mock the API response
    responses.add(
        responses.GET,
        f'https://fr24api.flightradar24.com/api/live/flight-details/{flight_id}',
        json=mock_response,
        status=200
    )

    # Make the request
    details = fr24_client.get_flight_details(flight_id)

    # Verify the response
    assert details == mock_response

@responses.activate
def test_get_historical_flight(fr24_client):
    """Test getting historical flight data."""
    flight_id = 'ABC123'
    date = datetime(2024, 3, 15)
    mock_response = {
        'data': {
            'id': flight_id,
            'date': '2024-03-15',
            'status': 'LANDED'
        }
    }

    # Mock the API response
    responses.add(
        responses.GET,
        f'https://fr24api.flightradar24.com/api/flights/historical/{flight_id}',
        json=mock_response,
        status=200
    )

    # Make the request
    historical_data = fr24_client.get_historical_flight(flight_id, date)

    # Verify the response
    assert historical_data == mock_response
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url.endswith('date=2024-03-15')

@responses.activate
def test_get_airport_details(fr24_client):
    """Test getting airport details."""
    airport_code = 'JFK'
    mock_response = {
        'data': {
            'code': airport_code,
            'name': 'John F. Kennedy International Airport',
            'city': 'New York'
        }
    }

    # Mock the API response
    responses.add(
        responses.GET,
        f'https://fr24api.flightradar24.com/api/airports/{airport_code}',
        json=mock_response,
        status=200
    )

    # Make the request
    airport_data = fr24_client.get_airport_details(airport_code)

    # Verify the response
    assert airport_data == mock_response

@responses.activate
def test_get_airline_details(fr24_client):
    """Test getting airline details."""
    airline_code = 'AAL'
    mock_response = {
        'data': {
            'code': airline_code,
            'name': 'American Airlines',
            'country': 'United States'
        }
    }

    # Mock the API response
    responses.add(
        responses.GET,
        f'https://fr24api.flightradar24.com/api/airlines/{airline_code}',
        json=mock_response,
        status=200
    )

    # Make the request
    airline_data = fr24_client.get_airline_details(airline_code)

    # Verify the response
    assert airline_data == mock_response 