import asyncio
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from ..config.db import get_db
from ..models.flight import Flight
from ..websockets.flight_socket import flight_manager
from .flightradar_client import FlightradarClient

# Constants for flight updates
UPDATE_INTERVAL_SECONDS = 30  # Update interval in seconds

# Initialize the Flightradar client
flightradar_client = FlightradarClient()

async def update_flight_positions():
    """
    Background task to update flight positions periodically using Flightradar API
    and broadcast to WebSocket clients.
    """
    while True:
        # Get a new database session
        db = next(get_db())
        try:
            # Get all active flights from the database
            active_flights = db.query(Flight).filter(Flight.status.in_(["ACTIVE", "EN_ROUTE", "DEPARTED"])).all()
            
            # Get flight data from Flightradar API
            live_flights = flightradar_client.get_live_flights()
            
            # Update flight positions based on Flightradar data
            updated_flights = update_flights_from_api(active_flights, live_flights, db)
            
            # Commit the changes
            db.commit()
            
            # Prepare the flight data for broadcasting
            flight_data = {
                "flights": [
                    {
                        "id": flight.id,
                        "flight_id": flight.flight_id,
                        "tail_number": flight.tail_number,
                        "status": flight.status,
                        "departure_time": flight.departure_time.isoformat() if flight.departure_time else None,
                        "arrival_time": flight.arrival_time.isoformat() if flight.arrival_time else None,
                        "current_position_lat": flight.current_position_lat,
                        "current_position_lon": flight.current_position_lon,
                        "altitude": flight.altitude,
                        "speed": flight.speed,
                        "heading": flight.heading
                    }
                    for flight in updated_flights
                ]
            }
            
            # Broadcast the updated flight data
            await flight_manager.broadcast(flight_data)
            
        except Exception as e:
            print(f"Error updating flight positions: {e}")
        finally:
            db.close()
        
        # Wait for the next update interval
        await asyncio.sleep(UPDATE_INTERVAL_SECONDS)

def update_flights_from_api(active_flights: List[Flight], live_flights: List[Dict[str, Any]], db: Session) -> List[Flight]:
    """
    Update flight positions based on data from the Flightradar API.
    
    Args:
        active_flights: List of active flights from the database
        live_flights: List of live flights from the Flightradar API
        db: Database session
        
    Returns:
        List of updated flights
    """
    # Create a mapping of flight IDs to live flight data
    live_flight_map = {
        flight['flight_id']: flight for flight in live_flights
    }
    
    # Create a mapping of tail numbers to live flight data as a fallback
    tail_number_map = {
        flight['tail_number']: flight for flight in live_flights if flight.get('tail_number')
    }
    
    updated_flights = []
    
    for flight in active_flights:
        # Try to find matching flight in live data
        live_flight = live_flight_map.get(flight.flight_id) or tail_number_map.get(flight.tail_number)
        
        if live_flight:
            # Update flight with live data
            flight.current_position_lat = live_flight.get('latitude', flight.current_position_lat)
            flight.current_position_lon = live_flight.get('longitude', flight.current_position_lon)
            flight.altitude = live_flight.get('altitude', flight.altitude)
            flight.speed = live_flight.get('speed', flight.speed)
            flight.heading = live_flight.get('heading', flight.heading)
            
            # Update status if available
            if live_flight.get('status'):
                flight.status = map_status(live_flight['status'])
            
            updated_flights.append(flight)
        else:
            # If no live data is available, fall back to simulation
            simulate_flight_position(flight)
            updated_flights.append(flight)
    
    return updated_flights

def simulate_flight_position(flight: Flight):
    """
    Simulate a flight's position if no live data is available.
    This is a fallback method when the API doesn't return data for a flight.
    """
    # Skip if the flight doesn't have position data
    if flight.current_position_lat is None or flight.current_position_lon is None:
        return
    
    # Add some small random movement
    flight.current_position_lat += random.uniform(-0.01, 0.01)
    flight.current_position_lon += random.uniform(-0.01, 0.01)
    
    # Add some randomness to altitude and speed
    flight.altitude += random.randint(-500, 500)
    flight.altitude = max(20000, min(40000, flight.altitude))  # Keep altitude within reasonable bounds
    
    flight.speed += random.randint(-20, 20)
    flight.speed = max(400, min(600, flight.speed))  # Keep speed within reasonable bounds

def map_status(api_status: str) -> str:
    """
    Map the status from the API to our internal status values.
    
    Args:
        api_status: Status from the API
        
    Returns:
        Mapped status for our application
    """
    status_map = {
        'en-route': 'EN_ROUTE',
        'scheduled': 'SCHEDULED',
        'landed': 'LANDED',
        'departed': 'DEPARTED',
        'diverted': 'DIVERTED',
        'cancelled': 'CANCELLED'
    }
    
    return status_map.get(api_status.lower(), 'ACTIVE') 