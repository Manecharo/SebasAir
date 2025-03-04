from sqlalchemy.orm import Session
from ..models.alert import Alert
from ..models.flight import Flight
from ..models.schedule import Schedule
from datetime import datetime, timedelta

def get_alerts(db: Session, resolved: bool = None):
    """
    Retrieve alerts from the database.
    If resolved is provided, filter by resolution status.
    """
    query = db.query(Alert)
    if resolved is not None:
        query = query.filter(Alert.is_resolved == resolved)
    return query.order_by(Alert.created_at.desc()).all()

def get_alert_by_id(db: Session, alert_id: int):
    """
    Retrieve a specific alert by ID.
    """
    return db.query(Alert).filter(Alert.id == alert_id).first()

def create_alert(db: Session, alert_data: dict):
    """
    Create a new alert.
    """
    db_alert = Alert(**alert_data)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def resolve_alert(db: Session, alert_id: int):
    """
    Mark an alert as resolved.
    """
    db_alert = get_alert_by_id(db, alert_id)
    if db_alert:
        db_alert.is_resolved = True
        db_alert.resolved_at = datetime.utcnow()
        db.commit()
        db.refresh(db_alert)
    return db_alert

def check_for_delays(db: Session, threshold_minutes: int = 15):
    """
    Check for flight delays exceeding the threshold.
    Creates alerts for any new delays found.
    """
    # Get scheduled flights for today
    today = datetime.utcnow().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    
    scheduled_flights = db.query(Schedule).filter(
        Schedule.scheduled_departure >= start_of_day,
        Schedule.scheduled_departure <= end_of_day
    ).all()
    
    # Check each scheduled flight against actual flights
    for scheduled in scheduled_flights:
        actual_flight = db.query(Flight).filter(
            Flight.flight_number == scheduled.flight_number,
            Flight.scheduled_departure >= start_of_day,
            Flight.scheduled_departure <= end_of_day
        ).first()
        
        if actual_flight and actual_flight.actual_departure:
            # Calculate delay in minutes
            scheduled_time = scheduled.scheduled_departure
            actual_time = actual_flight.actual_departure
            delay_minutes = (actual_time - scheduled_time).total_seconds() / 60
            
            if delay_minutes > threshold_minutes:
                # Check if an alert already exists for this flight
                existing_alert = db.query(Alert).filter(
                    Alert.flight_id == str(actual_flight.id),
                    Alert.type == 'delay',
                    Alert.is_resolved == False
                ).first()
                
                if not existing_alert:
                    # Create a new alert
                    alert_data = {
                        'type': 'delay',
                        'flight_id': str(actual_flight.id),
                        'details': f"Flight {actual_flight.flight_number} delayed by {int(delay_minutes)} minutes",
                        'severity': 'high' if delay_minutes > 30 else 'medium'
                    }
                    create_alert(db, alert_data)

def check_for_excessive_ground_time(db: Session, threshold_minutes: int = 60):
    """
    Check for flights with excessive ground time.
    Creates alerts for any new cases found.
    """
    # Implementation would depend on how ground time is tracked
    # This is a placeholder for the actual implementation
    pass

def check_for_route_deviations(db: Session):
    """
    Check for flights deviating from their planned routes.
    Creates alerts for any new deviations found.
    """
    # Implementation would depend on how routes are defined and tracked
    # This is a placeholder for the actual implementation
    pass 