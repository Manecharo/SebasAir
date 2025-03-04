from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class AlertType(str, Enum):
    DELAY = "delay"
    GROUND_TIME = "ground_time"
    ROUTE_DEVIATION = "route_deviation"
    MAINTENANCE = "maintenance"
    WEATHER = "weather"
    OTHER = "other"

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertBase(BaseModel):
    title: str
    description: str
    alert_type: AlertType
    severity: AlertSeverity
    flight_id: Optional[int] = None
    aircraft_id: Optional[int] = None
    related_entity_id: Optional[int] = None
    related_entity_type: Optional[str] = None

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: int
    created_at: datetime
    resolved_at: Optional[datetime] = None
    resolved: bool = False

    class Config:
        orm_mode = True 