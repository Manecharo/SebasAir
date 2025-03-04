import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.services.alert_service import (
    get_alerts,
    get_alert_by_id,
    create_alert,
    resolve_alert,
    check_for_delays
)
from src.models.alert import Alert
from src.models.flight import Flight
from src.models.schedule import Schedule

# Mock data
mock_alert_data = {
    "flight_id": "1",
    "type": "delay",
    "details": "Flight delayed by 20 minutes",
    "severity": "medium",
    "is_resolved": False
}

mock_alert = Alert(
    id=1,
    flight_id="1",
    type="delay",
    details="Flight delayed by 20 minutes",
    severity="medium",
    is_resolved=False,
    created_at=datetime.now(),
    resolved_at=None
)

mock_flight = Flight(
    id=1,
    flight_number="ABC123",
    departure_airport="JFK",
    arrival_airport="LAX",
    scheduled_departure=datetime.now() - timedelta(minutes=30),
    scheduled_arrival=datetime.now() + timedelta(hours=5),
    actual_departure=datetime.now() - timedelta(minutes=10),
    status="departed",
    latitude=40.7128,
    longitude=-74.0060,
    altitude=30000,
    speed=500,
    heading=90
)

mock_schedule = Schedule(
    id=1,
    flight_number="ABC123",
    scheduled_departure=datetime.now() - timedelta(minutes=30),
    scheduled_arrival=datetime.now() + timedelta(hours=5),
    departure_airport="JFK",
    arrival_airport="LAX"
)

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_get_alerts(mock_db):
    # Setup
    mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_alert]
    
    # Execute
    result = get_alerts(mock_db)
    
    # Assert
    assert len(result) == 1
    assert result[0].flight_id == "1"
    assert result[0].type == "delay"
    
    # Test with resolved filter
    mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
    result = get_alerts(mock_db, resolved=True)
    assert len(result) == 0

def test_get_alert_by_id(mock_db):
    # Setup
    mock_db.query.return_value.filter.return_value.first.return_value = mock_alert
    
    # Execute
    result = get_alert_by_id(mock_db, 1)
    
    # Assert
    assert result.id == 1
    assert result.flight_id == "1"
    
    # Test not found
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = get_alert_by_id(mock_db, 999)
    assert result is None

def test_create_alert(mock_db):
    # Setup
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    # Execute
    result = create_alert(mock_db, mock_alert_data)
    
    # Assert
    assert result.flight_id == "1"
    assert result.type == "delay"
    assert result.is_resolved is False
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_resolve_alert(mock_db):
    # Setup
    mock_alert_copy = MagicMock(spec=Alert)
    mock_alert_copy.id = 1
    mock_alert_copy.flight_id = "1"
    mock_alert_copy.type = "delay"
    mock_alert_copy.details = "Flight delayed by 20 minutes"
    mock_alert_copy.severity = "medium"
    mock_alert_copy.is_resolved = False
    mock_alert_copy.created_at = datetime.now()
    mock_alert_copy.resolved_at = None
    
    mock_db.query.return_value.filter.return_value.first.return_value = mock_alert_copy
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    # Execute
    result = resolve_alert(mock_db, 1)
    
    # Assert
    assert result.is_resolved is True
    assert result.resolved_at is not None
    mock_db.commit.assert_called_once()
    
    # Test not found
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = resolve_alert(mock_db, 999)
    assert result is None

@patch('src.services.alert_service.create_alert')
def test_check_for_delays(mock_create_alert, mock_db):
    # Setup
    today = datetime.utcnow().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    
    # Mock the schedule query
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_schedule]
    
    # Mock the flight query
    mock_db.query.return_value.filter.return_value.first.return_value = mock_flight
    
    # Mock the alert query
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Execute
    check_for_delays(mock_db)
    
    # Assert
    mock_create_alert.assert_called_once()
    
    # Test no delays
    mock_create_alert.reset_mock()
    mock_flight.actual_departure = mock_flight.scheduled_departure
    
    check_for_delays(mock_db)
    mock_create_alert.assert_not_called() 