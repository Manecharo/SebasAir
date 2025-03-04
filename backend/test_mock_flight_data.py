import sys
import logging
from src.services.mock_flight_data import MockFlightDataProvider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_mock_flight_data():
    """
    Test the mock flight data provider.
    """
    try:
        logger.info("Creating mock flight data provider...")
        provider = MockFlightDataProvider(num_flights=20)
        
        # Get live flights
        logger.info("Fetching live flights...")
        flights = provider.get_live_flights()
        logger.info(f"Successfully fetched {len(flights)} flights")
        
        # Print sample flight data
        if flights:
            sample_flight = flights[0]
            logger.info(f"Sample flight data: Flight {sample_flight['flight_id']} from {sample_flight['origin']} to {sample_flight['destination']}")
            logger.info(f"  Status: {sample_flight['status']}")
            logger.info(f"  Position: ({sample_flight['latitude']:.4f}, {sample_flight['longitude']:.4f})")
            logger.info(f"  Altitude: {sample_flight['altitude']} ft, Speed: {sample_flight['speed']} knots")
            
            # Get flight details
            flight_id = sample_flight['flight_id']
            logger.info(f"Fetching details for flight {flight_id}...")
            details = provider.get_flight_details(flight_id)
            
            logger.info(f"Flight details: {flight_id}")
            logger.info(f"  From: {details.get('origin_name')} ({details.get('origin_city')})")
            logger.info(f"  To: {details.get('destination_name')} ({details.get('destination_city')})")
            logger.info(f"  Distance: {details.get('distance')} km")
            logger.info(f"  Duration: {details.get('estimated_time_enroute')}")
            
            # Test filtering by bounds
            logger.info("Testing bounds filtering...")
            # Create a bounding box around the flight's current position
            lat, lon = sample_flight['latitude'], sample_flight['longitude']
            bounds = (lat - 5, lon - 5, lat + 5, lon + 5)
            filtered_flights = provider.get_live_flights(bounds)
            logger.info(f"Found {len(filtered_flights)} flights within the specified bounds")
            
            # Test position updates
            logger.info("Testing position updates...")
            provider._update_flight_positions()
            updated_flights = provider.get_live_flights()
            logger.info("Flight positions updated successfully")
            
            logger.info("All tests completed successfully!")
            return True
        else:
            logger.error("No flights were generated")
            return False
            
    except Exception as e:
        logger.error(f"Error testing mock flight data: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_mock_flight_data()
    sys.exit(0 if success else 1) 