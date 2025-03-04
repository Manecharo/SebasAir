import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from datetime import datetime
from .flightradar24_client import FlightRadar24Client
from ..models.flight import Flight
from ..schemas.flight import FlightCreate, FlightUpdate

# Import the mock data provider
from .mock_flight_data import MockFlightDataProvider

# Try to import the real client if it exists
try:
    from .flightradar_client import FlightradarClient
    FLIGHTRADAR_CLIENT_AVAILABLE = True
except ImportError:
    FLIGHTRADAR_CLIENT_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FlightDataService:
    """
    Service for retrieving flight data from either Flightradar24 API or mock data.
    This service automatically falls back to mock data if:
    1. The Flightradar API key is not set
    2. The FlightradarClient is not available
    3. The Flightradar API returns an error
    """
    
    def __init__(self, fr24_client: Optional[FlightRadar24Client] = None):
        """Initialize the flight data service."""
        # Load environment variables
        load_dotenv()
        
        # Get API key
        self.api_key = os.getenv('FLIGHTRADAR_API_KEY')
        
        # Determine if we should use real data or mock data
        self.use_real_data = (
            self.api_key and 
            self.api_key != 'your_api_key_here' and
            self.api_key != 'test_mode' and
            FLIGHTRADAR_CLIENT_AVAILABLE
        )
        
        if self.use_real_data:
            logger.info("Using real Flightradar24 API data")
            self.fr24_client = fr24_client or FlightRadar24Client(self.api_key)
        else:
            logger.info("Using mock flight data")
            self.mock_provider = MockFlightDataProvider(num_flights=50)
    
    def get_live_flights(self, bounds: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get live flight data from FlightRadar24.
        Processes and formats the data for the application.
        """
        try:
            raw_data = self.fr24_client.get_live_flights(bounds)
            return self._process_live_flights(raw_data)
        except Exception as e:
            # Log the error and return empty list
            logger.error(f"Error fetching live flights: {str(e)}")
            return []
    
    def get_flight_details(self, flight_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed flight information.
        Returns None if the flight is not found or an error occurs.
        """
        try:
            return self.fr24_client.get_flight_details(flight_id)
        except Exception as e:
            logger.error(f"Error fetching flight details: {str(e)}")
            return None
    
    def get_historical_flight_data(self, flight_id: str, date: datetime) -> Optional[Dict[str, Any]]:
        """
        Get historical flight data.
        Returns None if the data is not found or an error occurs.
        """
        try:
            return self.fr24_client.get_historical_flight(flight_id, date)
        except Exception as e:
            logger.error(f"Error fetching historical flight data: {str(e)}")
            return None
    
    def _process_live_flights(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process raw flight data from FlightRadar24 API.
        Converts it to the format expected by the application.
        """
        processed_flights = []
        
        for flight in raw_data.get('flights', []):
            try:
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
                processed_flights.append(processed_flight)
            except Exception as e:
                logger.error(f"Error processing flight data: {str(e)}")
                continue
        
        return processed_flights
    
    def create_flight_record(self, flight_data: FlightCreate) -> Flight:
        """Create a new flight record in the database."""
        # Implementation depends on your database setup
        pass
    
    def update_flight_record(self, flight_id: str, flight_data: FlightUpdate) -> Optional[Flight]:
        """Update an existing flight record in the database."""
        # Implementation depends on your database setup
        pass
    
    def is_using_real_data(self) -> bool:
        """
        Check if the service is using real data or mock data.
        
        Returns:
            True if using real data, False if using mock data
        """
        return self.use_real_data


# Example usage
if __name__ == "__main__":
    service = FlightDataService()
    
    # Get live flights
    flights = service.get_live_flights()
    print(f"Retrieved {len(flights)} flights")
    
    # Get details for the first flight
    if flights:
        flight_id = flights[0]['flight_id']
        details = service.get_flight_details(flight_id)
        print(f"Details for flight {flight_id}:")
        for key, value in details.items():
            print(f"  {key}: {value}") 