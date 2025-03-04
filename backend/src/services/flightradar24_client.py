import requests
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class FlightRadar24Client:
    """Client for interacting with the FlightRadar24 API."""
    
    def __init__(self, api_token: str):
        """Initialize the client with API token."""
        self.base_url = 'https://fr24api.flightradar24.com/api'
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_token}',
            'Accept-Version': 'v1'
        })

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the Flightradar24 API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to {url}: {e}")
            return {}

    def get_live_flights(self, bounds: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get live flight positions.
        
        Args:
            bounds: Optional bounding box coordinates (lat1,lat2,lon1,lon2)
            
        Returns:
            List of flight dictionaries
        """
        endpoint = '/live/flight-positions/light'
        params = {'bounds': bounds} if bounds else {}
        
        try:
            data = self._make_request(endpoint, params)
            flights = []
            
            for flight in data.get('data', []):
                processed_flight = {
                    'flight_id': flight.get('id'),
                    'callsign': flight.get('callsign'),
                    'registration': flight.get('registration'),
                    'aircraft_type': flight.get('aircraft', {}).get('type'),
                    'latitude': flight.get('latitude'),
                    'longitude': flight.get('longitude'),
                    'altitude': flight.get('altitude'),
                    'speed': flight.get('speed'),
                    'heading': flight.get('heading'),
                    'status': flight.get('status'),
                    'departure_airport': flight.get('departure', {}).get('code'),
                    'arrival_airport': flight.get('arrival', {}).get('code'),
                    'airline': flight.get('airline', {}).get('name'),
                    'last_updated': datetime.utcnow().isoformat()
                }
                flights.append(processed_flight)
            
            logger.info(f"Fetched {len(flights)} live flights from Flightradar24 API")
            return flights
        except Exception as e:
            logger.error(f"Error processing live flights data: {e}")
            return []

    def get_flight_details(self, flight_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific flight.
        
        Args:
            flight_id: The ID of the flight to fetch details for
            
        Returns:
            Dictionary containing detailed flight information
        """
        endpoint = f'/live/flight-details/{flight_id}'
        return self._make_request(endpoint)

    def get_historical_flight(self, flight_id: str, date: datetime) -> Dict[str, Any]:
        """
        Get historical flight data.
        
        Args:
            flight_id: The ID of the flight to fetch historical data for
            date: The date to fetch historical data for
            
        Returns:
            Dictionary containing historical flight information
        """
        endpoint = f'/flights/historical/{flight_id}'
        params = {'date': date.strftime('%Y-%m-%d')}
        return self._make_request(endpoint, params)

    def get_airport_details(self, airport_code: str) -> Dict[str, Any]:
        """
        Get detailed information about an airport.
        
        Args:
            airport_code: The IATA/ICAO code of the airport
            
        Returns:
            Dictionary containing airport information
        """
        endpoint = f'/airports/{airport_code}'
        return self._make_request(endpoint)

    def get_airline_details(self, airline_code: str) -> Dict[str, Any]:
        """
        Get detailed information about an airline.
        
        Args:
            airline_code: The IATA/ICAO code of the airline
            
        Returns:
            Dictionary containing airline information
        """
        endpoint = f'/airlines/{airline_code}'
        return self._make_request(endpoint) 