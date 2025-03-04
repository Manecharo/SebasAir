from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from ..config.db import Base
from datetime import datetime

class CompetitorFlight(Base):
    __tablename__ = 'competitor_flights'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    operator = Column(String, nullable=False)
    flight_number = Column(String, nullable=False)
    departure_airport = Column(String, nullable=False)
    arrival_airport = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)  # e.g., Scheduled, In-Flight, Completed
    aircraft_type = Column(String, nullable=True)
    remarks = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<CompetitorFlight(operator={self.operator}, flight_number={self.flight_number}, route={self.departure_airport}-{self.arrival_airport})>"
