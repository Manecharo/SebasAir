from sqlalchemy.orm import Session
from ..models.competitor import CompetitorFlight
from datetime import datetime, timedelta
from sqlalchemy import func

def get_competitor_flights(db: Session, date: datetime = None):
    """
    Retrieve competitor flights for a specific date.
    If no date is provided, returns today's competitor flights.
    """
    if date is None:
        date = datetime.utcnow().date()
    
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())
    
    return db.query(CompetitorFlight).filter(
        CompetitorFlight.departure_time >= start_of_day,
        CompetitorFlight.departure_time <= end_of_day
    ).all()

def get_competitor_flight_by_id(db: Session, flight_id: int):
    """
    Retrieve a specific competitor flight by ID.
    """
    return db.query(CompetitorFlight).filter(CompetitorFlight.id == flight_id).first()

def create_competitor_flight(db: Session, flight_data: dict):
    """
    Create a new competitor flight.
    """
    db_flight = CompetitorFlight(**flight_data)
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

def update_competitor_flight(db: Session, flight_id: int, flight_data: dict):
    """
    Update an existing competitor flight.
    """
    db_flight = get_competitor_flight_by_id(db, flight_id)
    if db_flight:
        for key, value in flight_data.items():
            setattr(db_flight, key, value)
        db_flight.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_flight)
    return db_flight

def delete_competitor_flight(db: Session, flight_id: int):
    """
    Delete a competitor flight.
    """
    db_flight = get_competitor_flight_by_id(db, flight_id)
    if db_flight:
        db.delete(db_flight)
        db.commit()
        return True
    return False

def get_competitor_stats(db: Session, date: datetime = None):
    """
    Get statistics about competitor flights for a specific date.
    """
    flights = get_competitor_flights(db, date)
    
    # Group flights by operator
    operators = {}
    for flight in flights:
        if flight.operator not in operators:
            operators[flight.operator] = {
                'total': 0,
                'completed': 0,
                'in_progress': 0,
                'scheduled': 0
            }
        
        operators[flight.operator]['total'] += 1
        
        if flight.status.lower() == 'completed':
            operators[flight.operator]['completed'] += 1
        elif flight.status.lower() == 'in-flight' or flight.status.lower() == 'in-progress':
            operators[flight.operator]['in_progress'] += 1
        else:
            operators[flight.operator]['scheduled'] += 1
    
    return {
        'total_flights': len(flights),
        'operators': operators
    }

def get_competitor_analytics(db: Session):
    """
    Get comprehensive analytics about competitor flights.
    Includes trends over time, route analysis, and market share.
    """
    # Get the last 30 days of data
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=30)
    
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    # Get all flights in the date range
    flights = db.query(CompetitorFlight).filter(
        CompetitorFlight.departure_time >= start_datetime,
        CompetitorFlight.departure_time <= end_datetime
    ).all()
    
    # Calculate market share by operator
    operator_counts = {}
    for flight in flights:
        if flight.operator not in operator_counts:
            operator_counts[flight.operator] = 0
        operator_counts[flight.operator] += 1
    
    total_flights = len(flights)
    market_share = {
        operator: {
            'count': count,
            'percentage': round((count / total_flights) * 100, 2) if total_flights > 0 else 0
        }
        for operator, count in operator_counts.items()
    }
    
    # Analyze routes
    route_analysis = {}
    for flight in flights:
        route_key = f"{flight.departure_airport}-{flight.arrival_airport}"
        if route_key not in route_analysis:
            route_analysis[route_key] = {
                'count': 0,
                'operators': set()
            }
        route_analysis[route_key]['count'] += 1
        route_analysis[route_key]['operators'].add(flight.operator)
    
    # Convert sets to lists for JSON serialization
    for route in route_analysis:
        route_analysis[route]['operators'] = list(route_analysis[route]['operators'])
    
    # Get daily flight counts for trend analysis
    daily_counts = []
    current_date = start_date
    while current_date <= end_date:
        day_start = datetime.combine(current_date, datetime.min.time())
        day_end = datetime.combine(current_date, datetime.max.time())
        
        day_count = db.query(func.count(CompetitorFlight.id)).filter(
            CompetitorFlight.departure_time >= day_start,
            CompetitorFlight.departure_time <= day_end
        ).scalar()
        
        daily_counts.append({
            'date': current_date.isoformat(),
            'count': day_count
        })
        
        current_date += timedelta(days=1)
    
    return {
        'total_flights': total_flights,
        'market_share': market_share,
        'route_analysis': route_analysis,
        'daily_trends': daily_counts
    } 