import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.services.competitor_service import (
    get_competitor_flights,
    get_competitor_flight_by_id,
    create_competitor_flight,
    get_competitor_flights_for_date,
    get_competitor_stats
)
from src.models.competitor_flight import CompetitorFlight

# Mock data
mock_competitor_flight_data = {
    "competitor_name": "Competitor A",
    "flight_id": "XYZ789",
    "tail_number": "N11111",
    "departure_time": datetime.now() - timedelta(hours=2),
    "arrival_time": datetime.now(),
    "origin": "JFK",
    "destination": "LAX"
}

mock_competitor_flight = CompetitorFlight(
    id=1,
    competitor_name="Competitor A",
    flight_id="XYZ789",
    tail_number="N11111",
    departure_time=datetime.now() - timedelta(hours=2),
    arrival_time=datetime.now(),
    origin="JFK",
    destination="LAX"
)

mock_competitor_flight2 = CompetitorFlight(
    id=2,
    competitor_name="Competitor B",
    flight_id="ABC456",
    tail_number="N22222",
    departure_time=datetime.now() - timedelta(hours=3),
    arrival_time=datetime.now() - timedelta(hours=1),
    origin="ORD",
    destination="DFW"
)

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_get_competitor_flights(mock_db):
    # Setup
    mock_db.query.return_value.all.return_value = [mock_competitor_flight, mock_competitor_flight2]
    
    # Execute
    result = get_competitor_flights(mock_db)
    
    # Assert
    assert len(result) == 2
    assert result[0].competitor_name == "Competitor A"
    assert result[1].competitor_name == "Competitor B"

def test_get_competitor_flight_by_id(mock_db):
    # Setup
    mock_db.query.return_value.filter.return_value.first.return_value = mock_competitor_flight
    
    # Execute
    result = get_competitor_flight_by_id(mock_db, 1)
    
    # Assert
    assert result.id == 1
    assert result.competitor_name == "Competitor A"
    assert result.flight_id == "XYZ789"
    
    # Test not found
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = get_competitor_flight_by_id(mock_db, 999)
    assert result is None

def test_create_competitor_flight(mock_db):
    # Setup
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    # Execute
    result = create_competitor_flight(mock_db, mock_competitor_flight_data)
    
    # Assert
    assert result.competitor_name == "Competitor A"
    assert result.flight_id == "XYZ789"
    assert result.origin == "JFK"
    assert result.destination == "LAX"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_get_competitor_flights_for_date(mock_db):
    # Setup
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_competitor_flight, mock_competitor_flight2]
    
    # Execute
    result = get_competitor_flights_for_date(mock_db, today)
    
    # Assert
    assert len(result) == 2
    
    # Test no flights for date
    mock_db.query.return_value.filter.return_value.all.return_value = []
    result = get_competitor_flights_for_date(mock_db, yesterday)
    assert len(result) == 0

def test_get_competitor_stats(mock_db):
    # Setup
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_competitor_flight, mock_competitor_flight2]
    
    # For the group by query
    mock_db.query.return_value.filter.return_value.group_by.return_value.all.return_value = [
        ("Competitor A", 1),
        ("Competitor B", 1)
    ]
    
    # For the route query
    mock_db.query.return_value.filter.return_value.group_by.return_value.having.return_value.all.return_value = [
        ("JFK", "LAX", 1),
        ("ORD", "DFW", 1)
    ]
    
    # Execute
    result = get_competitor_stats(mock_db)
    
    # Assert
    assert "total_flights" in result
    assert result["total_flights"] == 2
    assert "flights_by_competitor" in result
    assert len(result["flights_by_competitor"]) == 2
    assert "popular_routes" in result
    assert len(result["popular_routes"]) == 2
    
    # Test with date filter
    today = datetime.now().date()
    result = get_competitor_stats(mock_db, today)
    assert result["total_flights"] == 2 