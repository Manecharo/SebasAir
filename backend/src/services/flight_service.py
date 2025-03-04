from sqlalchemy.orm import Session
from ..models.flight import Flight
from datetime import datetime, timedelta
import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

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
def get_active_flights(db: Session):
    """
    Retrieve active flight data from the database.
    """
    return db.query(Flight).filter(Flight.status == 'active').all()

def get_flight_by_id(db: Session, flight_id: int):
    """
    Retrieve a specific flight by ID.
    """
    return db.query(Flight).filter(Flight.id == flight_id).first()

def get_flights_by_date(db: Session, date: datetime = None):
    """
    Retrieve flights for a specific date.
    If no date is provided, returns today's flights.
    """
    if date is None:
        date = datetime.utcnow().date()
    
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())
    
    return db.query(Flight).filter(
        Flight.scheduled_departure >= start_of_day,
        Flight.scheduled_departure <= end_of_day
    ).all()

def create_flight(db: Session, flight_data: dict):
    """
    Create a new flight.
    """
    db_flight = Flight(**flight_data)
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

def update_flight(db: Session, flight_id: int, flight_data: dict):
    """
    Update an existing flight.
    """
    db_flight = get_flight_by_id(db, flight_id)
    if db_flight:
        for key, value in flight_data.items():
            setattr(db_flight, key, value)
        db_flight.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_flight)
    return db_flight

def update_flight_position(db: Session, flight_id: int, latitude: float, longitude: float, altitude: float = None, heading: float = None, speed: float = None):
    """
    Update the position of a flight.
    """
    db_flight = get_flight_by_id(db, flight_id)
    if db_flight:
        db_flight.latitude = latitude
        db_flight.longitude = longitude
        if altitude is not None:
            db_flight.altitude = altitude
        if heading is not None:
            db_flight.heading = heading
        if speed is not None:
            db_flight.speed = speed
        db_flight.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_flight)
    return db_flight

def delete_flight(db: Session, flight_id: int):
    """
    Delete a flight.
    """
    db_flight = get_flight_by_id(db, flight_id)
    if db_flight:
        db.delete(db_flight)
        db.commit()
        return True
    return False
