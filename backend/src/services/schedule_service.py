from sqlalchemy.orm import Session
from ..models.schedule import Schedule
from ..models.flight import Flight
from datetime import datetime, timedelta, date
from typing import List, Dict, Any

def get_scheduled_flights(db: Session, date: datetime = None):
    """
    Retrieve scheduled flights for a specific date.
    If no date is provided, returns today's scheduled flights.
    """
    if date is None:
        date = datetime.utcnow().date()
    
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())
    
    return db.query(Schedule).filter(
        Schedule.scheduled_departure >= start_of_day,
        Schedule.scheduled_departure <= end_of_day
    ).all()

def get_schedule_by_id(db: Session, schedule_id: int):
    """
    Retrieve a specific scheduled flight by ID.
    """
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()

def create_schedule(db: Session, schedule_data: dict):
    """
    Create a new scheduled flight.
    """
    db_schedule = Schedule(**schedule_data)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def update_schedule(db: Session, schedule_id: int, schedule_data: dict):
    """
    Update an existing scheduled flight.
    """
    db_schedule = get_schedule_by_id(db, schedule_id)
    if db_schedule:
        for key, value in schedule_data.items():
            setattr(db_schedule, key, value)
        db_schedule.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_schedule)
    return db_schedule

def delete_schedule(db: Session, schedule_id: int):
    """
    Delete a scheduled flight.
    """
    db_schedule = get_schedule_by_id(db, schedule_id)
    if db_schedule:
        db.delete(db_schedule)
        db.commit()
        return True
    return False

def get_schedules_by_date(db: Session, query_date: date) -> List[Dict[str, Any]]:
    """
    Retrieve schedules for a specific date.
    Returns a list of schedule dictionaries with additional information.
    """
    start_of_day = datetime.combine(query_date, datetime.min.time())
    end_of_day = datetime.combine(query_date, datetime.max.time())
    
    schedules = db.query(Schedule).filter(
        Schedule.scheduled_departure >= start_of_day,
        Schedule.scheduled_departure <= end_of_day
    ).all()
    
    result = []
    for schedule in schedules:
        schedule_dict = {
            "id": schedule.id,
            "flight_number": schedule.flight_number,
            "departure_airport": schedule.departure_airport,
            "arrival_airport": schedule.arrival_airport,
            "scheduled_departure": schedule.scheduled_departure.isoformat() if schedule.scheduled_departure else None,
            "scheduled_arrival": schedule.scheduled_arrival.isoformat() if schedule.scheduled_arrival else None,
            "aircraft_id": schedule.aircraft_id,
            "created_at": schedule.created_at.isoformat() if schedule.created_at else None,
            "updated_at": schedule.updated_at.isoformat() if schedule.updated_at else None
        }
        result.append(schedule_dict)
    
    return result

def compare_schedules_with_flights(db: Session, query_date: date) -> List[Dict[str, Any]]:
    """
    Compare scheduled flights with actual flights for a specific date.
    Returns a list of dictionaries containing both schedule and actual flight information.
    """
    start_of_day = datetime.combine(query_date, datetime.min.time())
    end_of_day = datetime.combine(query_date, datetime.max.time())
    
    # Get all schedules for the date
    schedules = db.query(Schedule).filter(
        Schedule.scheduled_departure >= start_of_day,
        Schedule.scheduled_departure <= end_of_day
    ).all()
    
    result = []
    for schedule in schedules:
        # Find the corresponding actual flight
        flight = db.query(Flight).filter(
            Flight.flight_number == schedule.flight_number,
            Flight.scheduled_departure >= start_of_day,
            Flight.scheduled_departure <= end_of_day
        ).first()
        
        comparison = {
            "id": schedule.id,
            "flight_number": schedule.flight_number,
            "departure_airport": schedule.departure_airport,
            "arrival_airport": schedule.arrival_airport,
            "scheduled_departure": schedule.scheduled_departure.isoformat() if schedule.scheduled_departure else None,
            "scheduled_arrival": schedule.scheduled_arrival.isoformat() if schedule.scheduled_arrival else None,
            "aircraft_id": schedule.aircraft_id
        }
        
        if flight:
            comparison.update({
                "actual_departure": flight.actual_departure.isoformat() if flight.actual_departure else None,
                "actual_arrival": flight.actual_arrival.isoformat() if flight.actual_arrival else None,
                "status": flight.status,
                "delay_minutes": calculate_delay_minutes(schedule.scheduled_departure, flight.actual_departure) if flight.actual_departure else None
            })
        else:
            comparison.update({
                "actual_departure": None,
                "actual_arrival": None,
                "status": "Scheduled",
                "delay_minutes": None
            })
        
        result.append(comparison)
    
    return result

def calculate_delay_minutes(scheduled: datetime, actual: datetime) -> int:
    """
    Calculate the delay in minutes between scheduled and actual times.
    Returns a positive number for delays, negative for early departures.
    """
    if not scheduled or not actual:
        return None
    
    time_difference = actual - scheduled
    return int(time_difference.total_seconds() / 60) 