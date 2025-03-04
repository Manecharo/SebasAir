import pytest
import json
import os
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.services.report_service import (
    generate_daily_report,
    generate_weekly_report,
    export_report_to_json,
    export_report_to_csv
)
from src.models.flight import Flight
from src.models.schedule import Schedule
from src.models.competitor_flight import CompetitorFlight
from src.models.alert import Alert

# Mock data
mock_flights = [
    Flight(
        id=1,
        flight_id="ABC123",
        tail_number="N12345",
        status="COMPLETED",
        departure_time=datetime.now() - timedelta(hours=3),
        arrival_time=datetime.now() - timedelta(hours=1),
        current_position_lat=40.7128,
        current_position_lon=-74.0060,
        altitude=0,
        speed=0,
        heading=0
    ),
    Flight(
        id=2,
        flight_id="DEF456",
        tail_number="N67890",
        status="DELAYED",
        departure_time=datetime.now() - timedelta(minutes=30),
        arrival_time=None,
        current_position_lat=41.8781,
        current_position_lon=-87.6298,
        altitude=30000,
        speed=500,
        heading=90
    )
]

mock_schedules = [
    Schedule(
        id=1,
        flight_id="ABC123",
        tail_number="N12345",
        scheduled_departure=datetime.now() - timedelta(hours=3),
        scheduled_arrival=datetime.now() - timedelta(hours=1),
        origin="JFK",
        destination="LAX"
    ),
    Schedule(
        id=2,
        flight_id="DEF456",
        tail_number="N67890",
        scheduled_departure=datetime.now() - timedelta(hours=1),
        scheduled_arrival=datetime.now() + timedelta(hours=1),
        origin="ORD",
        destination="DFW"
    )
]

mock_competitor_flights = [
    CompetitorFlight(
        id=1,
        competitor_name="Competitor A",
        flight_id="XYZ789",
        tail_number="N11111",
        departure_time=datetime.now() - timedelta(hours=2),
        arrival_time=datetime.now(),
        origin="JFK",
        destination="LAX"
    )
]

mock_alerts = [
    Alert(
        id=1,
        flight_id="DEF456",
        alert_type="DELAY",
        description="Flight delayed by 30 minutes",
        severity="MEDIUM",
        is_resolved=False,
        created_at=datetime.now() - timedelta(hours=1),
        resolved_at=None
    )
]

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_generate_daily_report(mock_db):
    # Setup
    test_date = datetime.now().date()
    mock_db.query.return_value.filter.return_value.all.side_effect = [
        mock_flights, mock_schedules, mock_competitor_flights, mock_alerts
    ]
    
    # Execute
    report = generate_daily_report(mock_db, datetime.now())
    
    # Assert
    assert report["date"] == test_date.isoformat()
    assert report["total_flights"] == 2
    assert report["completed_flights"] == 1
    assert report["delayed_flights"] == 1
    assert "on_time_percentage" in report
    assert "average_delay" in report
    assert len(report["competitor_flights"]) == 1
    assert len(report["alerts"]) == 1

def test_generate_weekly_report(mock_db):
    # Setup
    with patch('src.services.report_service.generate_daily_report') as mock_daily_report:
        mock_daily_report.return_value = {
            "date": datetime.now().date().isoformat(),
            "total_flights": 2,
            "completed_flights": 1,
            "delayed_flights": 1,
            "on_time_percentage": 50.0,
            "average_delay": 30.0,
            "competitor_flights": [{"competitor_name": "Competitor A", "flight_count": 1}],
            "alerts": [{"alert_type": "DELAY", "count": 1}]
        }
        
        # Execute
        report = generate_weekly_report(mock_db, datetime.now())
        
        # Assert
        assert "start_date" in report
        assert "end_date" in report
        assert report["total_flights"] == 14  # 7 days * 2 flights per day
        assert report["completed_flights"] == 7  # 7 days * 1 completed flight per day
        assert report["delayed_flights"] == 7  # 7 days * 1 delayed flight per day
        assert report["on_time_percentage"] == 50.0
        assert report["average_delay"] == 30.0
        assert len(report["daily_reports"]) == 7
        assert len(report["competitor_summary"]) == 1
        assert len(report["alert_summary"]) == 1

@patch('builtins.open', new_callable=mock_open)
def test_export_report_to_json(mock_file):
    # Setup
    report = {
        "date": datetime.now().date().isoformat(),
        "total_flights": 2,
        "completed_flights": 1,
        "delayed_flights": 1
    }
    
    # Execute
    filename = export_report_to_json(report)
    
    # Assert
    assert "daily_report" in filename
    assert filename.endswith(".json")
    mock_file.assert_called_once()
    mock_file().write.assert_called_once_with(json.dumps(report, indent=4))

@patch('pandas.DataFrame.to_csv')
@patch('builtins.open', new_callable=mock_open)
def test_export_report_to_csv(mock_file, mock_to_csv):
    # Setup
    report = {
        "date": datetime.now().date().isoformat(),
        "total_flights": 2,
        "completed_flights": 1,
        "delayed_flights": 1,
        "flights": [
            {"flight_id": "ABC123", "status": "COMPLETED"},
            {"flight_id": "DEF456", "status": "DELAYED"}
        ]
    }
    
    # Execute
    filename = export_report_to_csv(report)
    
    # Assert
    assert "daily_report" in filename
    assert filename.endswith(".csv")
    mock_to_csv.assert_called_once() 