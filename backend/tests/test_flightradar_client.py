import pytest
from unittest.mock import patch, MagicMock
import json
import os
import requests
from src.services.flightradar_client import FlightradarClient

# Sample response data for mocking API calls
SAMPLE_FLIGHTS_RESPONSE = {
    "flights": {
        "ABC123": {
            "callsign": "ABC123",
            "registration": "N123AB",
            "aircraft": {
                "model": {
                    "code": "B738"
                }
            },
            "airport": {
                "origin": {
                    "code": {
                        "iata": "JFK"
                    }
                },
                "destination": {
                    "code": {
                        "iata": "LAX"
                    }
                }
            },
            "latitude": 40.7128,
            "longitude": -74.0060,
            "altitude": 35000,
            "speed": 450,
            "heading": 270,
            "status": "en-route",
            "airline": {
                "name": "Sample Airline"
            }
        }
    }
}

SAMPLE_FLIGHT_DETAILS_RESPONSE = {
    "flight": {
        "callsign": "ABC123",
        "registration": "N123AB",
        "aircraft": {
            "model": "Boeing 737-800",
            "code": "B738"
        },
        "status": "en-route",
        "position": {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "altitude": 35000,
            "speed": 450,
            "heading": 270
        }
    }
}

class TestFlightradarClient:
    """Tests for the FlightradarClient class."""
    
    @patch.dict(os.environ, {"FLIGHTRADAR_API_KEY": "test_api_key"})
    @patch('requests.Session.get')
    def test_get_live_flights(self, mock_get):
        """Test fetching live flights."""
        # Create a client instance for testing with mocked environment
        client = FlightradarClient()
        
        # Configure the mock to return a successful response
        mock_response = MagicMock()
        mock_response.json.return_value = SAMPLE_FLIGHTS_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the method
        flights = client.get_live_flights()
        
        # Verify the API was called correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs['params']['api_key'] == 'test_api_key'
        
        # Verify the response was processed correctly
        assert len(flights) == 1
        assert flights[0]['flight_id'] == 'ABC123'
        assert flights[0]['callsign'] == 'ABC123'
        assert flights[0]['tail_number'] == 'N123AB'
        assert flights[0]['origin'] == 'JFK'
        assert flights[0]['destination'] == 'LAX'
        assert flights[0]['latitude'] == 40.7128
        assert flights[0]['longitude'] == -74.0060
    
    @patch.dict(os.environ, {"FLIGHTRADAR_API_KEY": "test_api_key"})
    @patch('requests.Session.get')
    def test_get_flight_details(self, mock_get):
        """Test fetching flight details."""
        # Create a client instance for testing with mocked environment
        client = FlightradarClient()
        
        # Configure the mock to return a successful response
        mock_response = MagicMock()
        mock_response.json.return_value = SAMPLE_FLIGHT_DETAILS_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the method
        flight_details = client.get_flight_details('ABC123')
        
        # Verify the API was called correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs['params']['api_key'] == 'test_api_key'
        assert 'ABC123' in args[0]
        
        # Verify the response was processed correctly
        assert flight_details == SAMPLE_FLIGHT_DETAILS_RESPONSE['flight']
    
    @patch.dict(os.environ, {"FLIGHTRADAR_API_KEY": "test_api_key"})
    def test_api_error_handling_live_flights(self):
        """Test error handling when API request fails for live flights."""
        # Create a client instance for testing with mocked environment
        client = FlightradarClient()
        
        # Patch the session.get method directly on the client instance
        with patch.object(client.session, 'get', side_effect=requests.exceptions.RequestException("API Error")):
            # Call the method and verify it handles the error gracefully
            flights = client.get_live_flights()
            assert flights == []
    
    @patch.dict(os.environ, {"FLIGHTRADAR_API_KEY": "test_api_key"})
    def test_api_error_handling_flight_details(self):
        """Test error handling when API request fails for flight details."""
        # Create a client instance for testing with mocked environment
        client = FlightradarClient()
        
        # Patch the session.get method directly on the client instance
        with patch.object(client.session, 'get', side_effect=requests.exceptions.RequestException("API Error")):
            # Test error handling for flight details
            flight_details = client.get_flight_details('ABC123')
            assert flight_details == {} 