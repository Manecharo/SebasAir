import os
import sys
import logging
from dotenv import load_dotenv
from .flightradar_client import FlightradarClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    client = FlightradarClient()
    
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