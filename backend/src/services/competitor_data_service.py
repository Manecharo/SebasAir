import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime, time

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .competitor_data_client import CompetitorDataClient
from ..config.db import SessionLocal
from ..models.competitor import CompetitorFlight

logger = logging.getLogger(__name__)

class CompetitorDataService:
    """
    Service to fetch competitor flight data daily and store it in the database.
    """
    def __init__(self, fetch_time: time = time(0, 0), interval_seconds: int = 86400):
        """
        Initialize the service.

        Args:
            fetch_time: Time of day to perform the fetch (default: midnight)
            interval_seconds: Interval between fetches in seconds (default: 86400 seconds = 24 hours)
        """
        self.fetch_time = fetch_time
        self.interval_seconds = interval_seconds
        self.client = CompetitorDataClient()

    async def fetch_and_store_competitor_flights(self):
        """
        Fetch competitor flights and store them in the database.
        """
        try:
            flights: List[Dict[str, Any]] = self.client.get_daily_competitor_flights()
            if not flights:
                logger.warning("No competitor flights fetched from Competitor API.")
                return

            db: Session = SessionLocal()
            try:
                for flight_data in flights:
                    # Check if flight already exists to prevent duplicates
                    existing_flight = db.query(CompetitorFlight).filter_by(
                        flight_number=flight_data.get("flight_number"),
                        departure_time=flight_data.get("departure_time")
                    ).first()
                    if existing_flight:
                        # Update existing flight data
                        for key, value in flight_data.items():
                            setattr(existing_flight, key, value)
                    else:
                        # Create new competitor flight entry
                        competitor_flight = CompetitorFlight(
                            operator=flight_data.get("operator"),
                            flight_number=flight_data.get("flight_number"),
                            route=flight_data.get("route"),
                            departure_time=flight_data.get("departure_time"),
                            arrival_time=flight_data.get("arrival_time"),
                            status=flight_data.get("status"),
                            aircraft_type=flight_data.get("aircraft_type"),
                            remarks=flight_data.get("remarks")
                        )
                        db.add(competitor_flight)
                db.commit()
                logger.info(f"Stored/Updated {len(flights)} competitor flights in the database.")
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Database error while storing competitor flights: {e}")
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Unexpected error in fetch_and_store_competitor_flights: {e}")

    async def schedule_daily_fetch(self):
        """
        Schedule the daily competitor flight data fetch at the specified time.
        """
        while True:
            now = datetime.now().time()
            today = datetime.now()

            # Calculate the next run time
            run_time = datetime.combine(today.date(), self.fetch_time)
            if now > self.fetch_time:
                run_time = run_time.replace(day=run_time.day + 1)

            wait_seconds = (run_time - datetime.now()).total_seconds()
            logger.info(f"CompetitorDataService will fetch data in {wait_seconds} seconds at {run_time.time()}.")

            await asyncio.sleep(wait_seconds)
            await self.fetch_and_store_competitor_flights()

    async def run(self):
        """
        Start the scheduled daily fetch.
        """
        await self.schedule_daily_fetch()

def start_competitor_data_service():
    """
    Start the competitor data service.
    """
    service = CompetitorDataService()
    loop = asyncio.get_event_loop()
    loop.create_task(service.run())
    logger.info("Competitor data service started.")
