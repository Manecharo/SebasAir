from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..config.db import Base
from datetime import datetime
import enum

class FlightStatus(enum.Enum):
    SCHEDULED = "scheduled"
    DEPARTED = "departed"
    EN_ROUTE = "en_route"
    ARRIVED = "arrived"
    CANCELLED = "cancelled"
    DELAYED = "delayed"

class Flight(Base):
    __tablename__ = 'flights'
    
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, index=True)
    departure_airport = Column(String)
    arrival_airport = Column(String)
    scheduled_departure = Column(DateTime, nullable=True)
    scheduled_arrival = Column(DateTime, nullable=True)
    actual_departure = Column(DateTime, nullable=True)
    actual_arrival = Column(DateTime, nullable=True)
    status = Column(String, default="scheduled")  # scheduled, departed, en_route, arrived, delayed, cancelled
    aircraft_id = Column(String, ForeignKey("aircraft.id"), nullable=True)
    
    # Position data
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    altitude = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)
    heading = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    aircraft = relationship("Aircraft", back_populates="flights")
    alerts = relationship("Alert", back_populates="flight")
    
    def __repr__(self):
        return f"<Flight {self.flight_number} from {self.departure_airport} to {self.arrival_airport}>"
