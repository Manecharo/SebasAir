from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..config.db import Base
from datetime import datetime

class Schedule(Base):
    __tablename__ = 'schedules'
    
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, nullable=False)
    departure_airport = Column(String, nullable=False)
    arrival_airport = Column(String, nullable=False)
    scheduled_departure = Column(DateTime, nullable=False)
    scheduled_arrival = Column(DateTime, nullable=False)
    aircraft_type = Column(String, nullable=False)
    tail_number = Column(String, nullable=False)
    status = Column(String, default='scheduled')  # scheduled, active, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Schedule {self.flight_number} {self.departure_airport}-{self.arrival_airport} {self.scheduled_departure}>" 