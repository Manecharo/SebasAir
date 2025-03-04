import requests
from typing import List, Dict, Any
import os
import logging

logger = logging.getLogger(__name__)

class OpenSkyClient:
    """
    Client to interact with the OpenSky API for fetching live flight data.
    """
    BASE_URL = "https://opensky-network.org/api"

    def __init__(self):
        self.session = requests.Session()
        # If authentication is required in the future, credentials can be loaded from environment variables
        # self.username = os.getenv('OPENSKY_USERNAME')
        # self.password = os.getenv('OPENSKY_PASSWORD')
        # self.session.auth = (self.username, self.password)

    def get_live_flights(self) -> List[Dict[str, Any]]:
        """
        Fetches live flight data from the OpenSky API.

        Returns:
            List of dictionaries containing flight data.
        """
        url = f"{self.BASE_URL}/states/all"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            states = data.get("states", [])
            flights = []
            for state in states:
                flight = {
                    "icao24": state[0],
                    "callsign": state[1].strip() if state[1] else None,
                    "origin_country": state[2],
                    "time_position": state[3],
                    "last_contact": state[4],
                    "longitude": state[5],
                    "latitude": state[6],
                    "baro_altitude": state[7],
                    "on_ground": state[8],
                    "velocity": state[9],
                    "heading": state[10],
                    "vertical_rate": state[11],
                    "sensors": state[12],
                    "geo_altitude": state[13],
                    "squawk": state[14],
                    "spi": state[15],
                    "position_source": state[16],
                }
                flights.append(flight)
            logger.info(f"Fetched {len(flights)} live flights from OpenSky API.")
            return flights
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching live flights from OpenSky API: {e}")
            return []
