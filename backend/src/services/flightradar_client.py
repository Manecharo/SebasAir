import requests
from typing import List, Dict, Any
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class FlightradarClient:
    """
    Client to interact with the Flightradar24 API for fetching live flight data.
    """
    BASE_URL = "https://api.flightradar24.com/v1"

    def __init__(self, api_key=None):
        self.session = requests.Session()
        self.api_key = api_key or os.getenv('FLIGHTRADAR_API_KEY')
        if not self.api_key:
            logger.warning("FLIGHTRADAR_API_KEY environment variable not set. API calls may fail.")

    def get_live_flights(self, bounds=None) -> List[Dict[str, Any]]:
        """
        Fetches live flight data from the Flightradar24 API.

        Args:
            bounds (tuple, optional): Bounding box for filtering flights (lat1, lon1, lat2, lon2).
                                     Default is None (global).

        Returns:
            List of dictionaries containing flight data.
        """
        url = f"{self.BASE_URL}/flights"
        params = {
            'api_key': self.api_key
        }
        
        if bounds:
            params['bounds'] = ','.join(map(str, bounds))
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            flights = []
            
            # Process the response based on Flightradar24 API structure
            # Note: Adjust this based on the actual API response structure
            for flight_id, flight_data in data.get('flights', {}).items():
                flight = {
                    'flight_id': flight_id,
                    'callsign': flight_data.get('callsign'),
                    'tail_number': flight_data.get('registration'),
                    'aircraft_type': flight_data.get('aircraft', {}).get('model', {}).get('code'),
                    'origin': flight_data.get('airport', {}).get('origin', {}).get('code', {}).get('iata'),
                    'destination': flight_data.get('airport', {}).get('destination', {}).get('code', {}).get('iata'),
                    'latitude': flight_data.get('latitude'),
                    'longitude': flight_data.get('longitude'),
                    'altitude': flight_data.get('altitude'),
                    'speed': flight_data.get('speed'),
                    'heading': flight_data.get('heading'),
                    'status': flight_data.get('status'),
                    'airline': flight_data.get('airline', {}).get('name')
                }
                flights.append(flight)
            
            logger.info(f"Fetched {len(flights)} live flights from Flightradar24 API.")
            return flights
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching live flights from Flightradar24 API: {e}")
            return []
    
    def get_flight_details(self, flight_id: str) -> Dict[str, Any]:
        """
        Fetches detailed information for a specific flight.

        Args:
            flight_id (str): The ID of the flight to fetch details for.

        Returns:
            Dictionary containing detailed flight information.
        """
        url = f"{self.BASE_URL}/flights/{flight_id}"
        params = {
            'api_key': self.api_key
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Process the response based on Flightradar24 API structure
            # Note: Adjust this based on the actual API response structure
            flight_details = data.get('flight', {})
            
            logger.info(f"Fetched details for flight {flight_id} from Flightradar24 API.")
            return flight_details
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching flight details from Flightradar24 API: {e}")
            return {} 