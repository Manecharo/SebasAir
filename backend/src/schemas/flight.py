from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FlightBase(BaseModel):
    """Base flight schema with common attributes."""
    callsign: Optional[str] = None
    registration: Optional[str] = None
    aircraft_type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    speed: Optional[float] = None
    heading: Optional[float] = None
    status: Optional[str] = None
    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    airline: Optional[str] = None

class FlightCreate(FlightBase):
    """Schema for creating a new flight record."""
    flight_id: str = Field(..., description="Unique flight identifier")
    scheduled_departure: Optional[datetime] = None
    scheduled_arrival: Optional[datetime] = None

class FlightUpdate(FlightBase):
    """Schema for updating an existing flight record."""
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    status_update: Optional[str] = None

class FlightResponse(FlightBase):
    """Schema for flight response data."""
    flight_id: str
    last_updated: datetime
    
    class Config:
        orm_mode = True

class FlightDetails(FlightResponse):
    """Schema for detailed flight information."""
    scheduled_departure: Optional[datetime] = None
    scheduled_arrival: Optional[datetime] = None
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    route: Optional[str] = None
    equipment: Optional[str] = None
    flight_number: Optional[str] = None
    delay: Optional[int] = None
    
    class Config:
        orm_mode = True

class FlightHistorical(FlightDetails):
    """Schema for historical flight data."""
    date: datetime
    track_points: Optional[list] = None
    events: Optional[list] = None
    
    class Config:
        orm_mode = True 