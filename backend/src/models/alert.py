from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
from ..config.db import Base

class AlertType(enum.Enum):
    DELAY = "delay"
    GROUND_TIME = "ground_time"
    ROUTE_DEVIATION = "route_deviation"
    MAINTENANCE = "maintenance"
    WEATHER = "weather"
    OTHER = "other"

class AlertSeverity(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    alert_type = Column(Enum(AlertType), nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False)
    
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=True)
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"), nullable=True)
    
    related_entity_id = Column(Integer, nullable=True)
    related_entity_type = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    resolved = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    flight = relationship("Flight", back_populates="alerts")
    aircraft = relationship("Aircraft", back_populates="alerts")

    def __repr__(self):
        return f"<Alert {self.title}: {self.description}>"
