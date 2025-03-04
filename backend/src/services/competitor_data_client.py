import requests
from typing import List, Dict, Any
import os
import logging

logger = logging.getLogger(__name__)

class CompetitorDataClient:
    """
    Client to interact with the Competitor Flight Data API.
    """
    BASE_URL = "https://api.competitor-flight-data.com/v1"

    def __init__(self):
        self.session = requests.Session()
        self.api_key = os.getenv('COMPETITOR_API_KEY')
        if not self.api_key:
            logger.error("COMPETITOR_API_KEY environment variable is not set.")
            raise ValueError("COMPETITOR_API_KEY environment variable is required.")
        self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})

    def get_daily_competitor_flights(self) -> List[Dict[str, Any]]:
        """
        Fetches daily competitor flight data from the Competitor API.

        Returns:
            List of dictionaries containing competitor flight data.
        """
        url = f"{self.BASE_URL}/flights/daily"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            flights = data.get("flights", [])
            logger.info(f"Fetched {len(flights)} competitor flights from Competitor API.")
            return flights
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching competitor flights from Competitor API: {e}")
            return []
