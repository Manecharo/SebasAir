from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..services.flight_data_service import FlightDataService
from ..schemas.flight import FlightResponse, FlightCreate, FlightUpdate

router = APIRouter(prefix="/api/flights", tags=["flights"])

def get_flight_service() -> FlightDataService:
    """Dependency injection for FlightDataService."""
    return FlightDataService()

@router.get("/live", response_model=List[FlightResponse])
async def get_live_flights(
    bounds: Optional[str] = Query(None, description="Bounding box coordinates (lat1,lat2,lon1,lon2)"),
    service: FlightDataService = Depends(get_flight_service)
):
    """
    Get live flight data within specified bounds.
    If no bounds are specified, returns all available flights.
    """
    try:
        flights = service.get_live_flights(bounds)
        return flights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{flight_id}", response_model=Dict[str, Any])
async def get_flight_details(
    flight_id: str,
    service: FlightDataService = Depends(get_flight_service)
):
    """Get detailed information about a specific flight."""
    try:
        flight_details = service.get_flight_details(flight_id)
        if not flight_details:
            raise HTTPException(status_code=404, detail="Flight not found")
        return flight_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historical/{flight_id}", response_model=Dict[str, Any])
async def get_historical_flight_data(
    flight_id: str,
    date: datetime = Query(..., description="Date for historical data (YYYY-MM-DD)"),
    service: FlightDataService = Depends(get_flight_service)
):
    """Get historical data for a specific flight on a given date."""
    try:
        historical_data = service.get_historical_flight_data(flight_id, date)
        if not historical_data:
            raise HTTPException(status_code=404, detail="Historical flight data not found")
        return historical_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=FlightResponse)
async def create_flight(
    flight_data: FlightCreate,
    service: FlightDataService = Depends(get_flight_service)
):
    """Create a new flight record."""
    try:
        flight = service.create_flight_record(flight_data)
        return flight
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{flight_id}", response_model=FlightResponse)
async def update_flight(
    flight_id: str,
    flight_data: FlightUpdate,
    service: FlightDataService = Depends(get_flight_service)
):
    """Update an existing flight record."""
    try:
        flight = service.update_flight_record(flight_id, flight_data)
        if not flight:
            raise HTTPException(status_code=404, detail="Flight not found")
        return flight
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 