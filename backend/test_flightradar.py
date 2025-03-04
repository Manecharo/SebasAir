import os
import sys
import logging
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleFlightradarClient:
    """
    Simplified client to test the Flightradar24 API.
    """
    BASE_URL = "https://api.flightradar24.com/v1"

    def __init__(self, api_key):
        self.session = requests.Session()
        self.api_key = api_key

    def get_live_flights(self, bounds=None):
        """
        Fetches live flight data from the Flightradar24 API.
        """
        url = f"{self.BASE_URL}/flights"
        params = {
            'api_key': self.api_key
        }
        
        if bounds:
            params['bounds'] = ','.join(map(str, bounds))
        
        try:
            logger.info(f"Making request to {url}")
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Log the raw response structure
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dictionary'}")
            
            flights = []
            
            # Process the response based on Flightradar24 API structure
            if 'flights' in data and isinstance(data['flights'], dict):
                for flight_id, flight_data in data['flights'].items():
                    flight = {
                        'flight_id': flight_id,
                        'callsign': flight_data.get('callsign'),
                        'tail_number': flight_data.get('registration'),
                        'latitude': flight_data.get('latitude'),
                        'longitude': flight_data.get('longitude'),
                        'altitude': flight_data.get('altitude'),
                        'speed': flight_data.get('speed'),
                        'heading': flight_data.get('heading'),
                        'status': flight_data.get('status')
                    }
                    flights.append(flight)
            
            logger.info(f"Processed {len(flights)} flights from response")
            return flights
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching live flights from Flightradar24 API: {e}")
            return []

def test_flightradar_api():
    """
    Test the Flightradar API key by making a simple request.
    """
    # Load environment variables
    load_dotenv()
    
    # Get the API key
    api_key = os.getenv('FLIGHTRADAR_API_KEY')
    if not api_key:
        logger.error("FLIGHTRADAR_API_KEY environment variable not set.")
        return False
    
    logger.info(f"Using API key: {api_key[:10]}...{api_key[-10:]}")
    
    # Create a client
    client = SimpleFlightradarClient(api_key)
    
    # Try to fetch live flights
    flights = client.get_live_flights()
    
    if flights:
        logger.info(f"Successfully fetched {len(flights)} flights from Flightradar API.")
        # Print some sample flight data
        if len(flights) > 0:
            logger.info("Sample flight data:")
            sample_flight = flights[0]
            for key, value in sample_flight.items():
                logger.info(f"  {key}: {value}")
        return True
    else:
        logger.error("Failed to fetch flights from Flightradar API.")
        return False

if __name__ == "__main__":
    success = test_flightradar_api()
    sys.exit(0 if success else 1) 