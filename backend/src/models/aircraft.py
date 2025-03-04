from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..config.db import Base

class Aircraft(Base):
    __tablename__ = "aircraft"

    id = Column(String, primary_key=True, index=True)
    registration = Column(String, unique=True, index=True)
    model = Column(String)
    manufacturer = Column(String)
    year_manufactured = Column(Integer, nullable=True)
    capacity = Column(Integer, nullable=True)
    range_km = Column(Float, nullable=True)
    max_speed_kts = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    flights = relationship("Flight", back_populates="aircraft")
    alerts = relationship("Alert", back_populates="aircraft")
    
    def __repr__(self):
        return f"<Aircraft {self.registration} ({self.model})>" 