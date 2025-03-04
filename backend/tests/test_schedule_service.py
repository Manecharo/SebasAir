import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.services.schedule_service import (
    get_schedules,
    get_schedule_by_id,
    create_schedule,
    update_schedule,
    get_schedules_for_date,
    get_schedule_comparison
)
from src.models.schedule import Schedule
from src.models.flight import Flight

# Mock data
mock_schedule_data = {
    "flight_id": "ABC123",
    "tail_number": "N12345",
    "scheduled_departure": datetime.now() + timedelta(hours=1),
    "scheduled_arrival": datetime.now() + timedelta(hours=3),
    "origin": "JFK",
    "destination": "LAX"
}

mock_schedule = Schedule(
    id=1,
    flight_id="ABC123",
    tail_number="N12345",
    scheduled_departure=datetime.now() + timedelta(hours=1),
    scheduled_arrival=datetime.now() + timedelta(hours=3),
    origin="JFK",
    destination="LAX"
)

mock_past_schedule = Schedule(
    id=2,
    flight_id="DEF456",
    tail_number="N67890",
    scheduled_departure=datetime.now() - timedelta(hours=3),
    scheduled_arrival=datetime.now() - timedelta(hours=1),
    origin="ORD",
    destination="DFW"
)

mock_flight = Flight(
    id=1,
    flight_id="ABC123",
    tail_number="N12345",
    status="SCHEDULED",
    departure_time=None,
    arrival_time=None,
    current_position_lat=None,
    current_position_lon=None,
    altitude=None,
    speed=None,
    heading=None
)

mock_active_flight = Flight(
    id=2,
    flight_id="DEF456",
    tail_number="N67890",
    status="ACTIVE",
    departure_time=datetime.now() - timedelta(hours=2, minutes=45),  # 15 min delay
    arrival_time=None,
    current_position_lat=41.8781,
    current_position_lon=-87.6298,
    altitude=30000,
    speed=500,
    heading=90
)

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_get_schedules(mock_db):
    # Setup
    mock_db.query.return_value.all.return_value = [mock_schedule, mock_past_schedule]
    
    # Execute
    result = get_schedules(mock_db)
    
    # Assert
    assert len(result) == 2
    assert result[0].flight_id == "ABC123"
    assert result[1].flight_id == "DEF456"

def test_get_schedule_by_id(mock_db):
    # Setup
    mock_db.query.return_value.filter.return_value.first.return_value = mock_schedule
    
    # Execute
    result = get_schedule_by_id(mock_db, 1)
    
    # Assert
    assert result.id == 1
    assert result.flight_id == "ABC123"
    
    # Test not found
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = get_schedule_by_id(mock_db, 999)
    assert result is None

def test_create_schedule(mock_db):
    # Setup
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    # Execute
    result = create_schedule(mock_db, mock_schedule_data)
    
    # Assert
    assert result.flight_id == "ABC123"
    assert result.tail_number == "N12345"
    assert result.origin == "JFK"
    assert result.destination == "LAX"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_update_schedule(mock_db):
    # Setup
    mock_db.query.return_value.filter.return_value.first.return_value = mock_schedule
    mock_db.commit.return_value = None
    
    update_data = {
        "scheduled_departure": datetime.now() + timedelta(hours=2),
        "scheduled_arrival": datetime.now() + timedelta(hours=4),
        "origin": "LGA"
    }
    
    # Execute
    result = update_schedule(mock_db, 1, update_data)
    
    # Assert
    assert result.origin == "LGA"
    assert result.destination == "LAX"  # Unchanged
    mock_db.commit.assert_called_once()
    
    # Test not found
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = update_schedule(mock_db, 999, update_data)
    assert result is None

def test_get_schedules_for_date(mock_db):
    # Setup
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_schedule]
    
    # Execute
    result = get_schedules_for_date(mock_db, tomorrow)
    
    # Assert
    assert len(result) == 1
    assert result[0].flight_id == "ABC123"
    
    # Test no schedules for date
    mock_db.query.return_value.filter.return_value.all.return_value = []
    result = get_schedules_for_date(mock_db, today - timedelta(days=7))
    assert len(result) == 0

def test_get_schedule_comparison(mock_db):
    # Setup
    mock_db.query.return_value.outerjoin.return_value.all.return_value = [
        (mock_past_schedule, mock_active_flight),
        (mock_schedule, None)
    ]
    
    # Execute
    result = get_schedule_comparison(mock_db)
    
    # Assert
    assert len(result) == 2
    
    # Check the completed flight with delay
    assert result[0]["flight_id"] == "DEF456"
    assert result[0]["status"] == "ACTIVE"
    assert result[0]["is_delayed"] is True
    assert result[0]["delay_minutes"] == 15
    
    # Check the scheduled flight not yet departed
    assert result[1]["flight_id"] == "ABC123"
    assert result[1]["status"] == "SCHEDULED"
    assert result[1]["is_delayed"] is False
    assert result[1]["delay_minutes"] == 0 