import asyncio
import logging
from typing import List, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .open_sky_client import OpenSkyClient
from ..config.db import SessionLocal
from ..models.flight import Flight

logger = logging.getLogger(__name__)

class FlightDataService:
    """
    Background service to fetch flight data periodically and store it in the database.
    """
    def __init__(self, interval: int = 300):
        """
        Initialize the service.

        Args:
            interval: Time between fetches in seconds (default: 300 seconds = 5 minutes)
        """
        self.interval = interval
        self.client = OpenSkyClient()

    async def fetch_and_store_flights(self):
        """
        Fetch flights and store them in the database.
        """
        try:
            flights: List[Dict[str, Any]] = self.client.get_live_flights()
            if not flights:
                logger.warning("No flights fetched from OpenSky API.")
                return

            db: Session = SessionLocal()
            try:
                for flight_data in flights:
                    # Check if flight already exists to prevent duplicates
                    existing_flight = db.query(Flight).filter_by(icao24=flight_data.get("icao24")).first()
                    if existing_flight:
                        # Update existing flight data
                        for key, value in flight_data.items():
                            setattr(existing_flight, key, value)
                    else:
                        # Create new flight entry
                        flight = Flight(
                            icao24=flight_data.get("icao24"),
                            callsign=flight_data.get("callsign"),
                            origin_country=flight_data.get("origin_country"),
                            time_position=flight_data.get("time_position"),
                            last_contact=flight_data.get("last_contact"),
                            longitude=flight_data.get("longitude"),
                            latitude=flight_data.get("latitude"),
                            baro_altitude=flight_data.get("baro_altitude"),
                            on_ground=flight_data.get("on_ground"),
                            velocity=flight_data.get("velocity"),
                            heading=flight_data.get("heading"),
                            vertical_rate=flight_data.get("vertical_rate"),
                            sensors=flight_data.get("sensors"),
                            geo_altitude=flight_data.get("geo_altitude"),
                            squawk=flight_data.get("squawk"),
                            spi=flight_data.get("spi"),
                            position_source=flight_data.get("position_source"),
                        )
                        db.add(flight)
                db.commit()
                logger.info(f"Stored/Updated {len(flights)} flights in the database.")
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Database error while storing flights: {e}")
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Unexpected error in fetch_and_store_flights: {e}")

    async def run(self):
        """
        Periodically fetch and store flight data.
        """
        while True:
            await self.fetch_and_store_flights()
            await asyncio.sleep(self.interval)

def start_flight_data_service():
    """
    Start the background flight data service.
    """
    service = FlightDataService()
    loop = asyncio.get_event_loop()
    loop.create_task(service.run())
    logger.info("Flight data service started.")
