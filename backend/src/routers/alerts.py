from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from ..config.db import get_db
from ..models.alert import Alert
from ..schemas.alert import AlertCreate, AlertResponse
from ..services import alert_service

router = APIRouter(
    prefix="/api/alerts",
    tags=["alerts"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[AlertResponse])
def get_alerts(
    resolved: Optional[bool] = Query(None, description="Filter by resolution status"),
    db: Session = Depends(get_db)
):
    """
    Retrieve alerts with optional filtering by resolution status.
    """
    try:
        alerts = alert_service.get_alerts(db, resolved)
        return {"alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific alert by ID.
    """
    try:
        alert = alert_service.get_alert_by_id(db, alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail=f"Alert with ID {alert_id} not found")
        return alert
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=AlertResponse, status_code=201)
def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new alert.
    """
    try:
        alert = alert_service.create_alert(db, alert_data.dict())
        return alert
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """
    Mark an alert as resolved.
    """
    try:
        alert = alert_service.resolve_alert(db, alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail=f"Alert with ID {alert_id} not found")
        return alert
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/check/delays")
def check_for_delays(
    threshold_minutes: int = Query(15, description="Delay threshold in minutes"),
    db: Session = Depends(get_db)
):
    """
    Check for flight delays exceeding the threshold and create alerts.
    """
    try:
        alerts = alert_service.check_for_delays(db, threshold_minutes)
        return {"alerts_created": len(alerts), "alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/check/ground-time")
def check_for_excessive_ground_time(
    threshold_minutes: int = Query(60, description="Ground time threshold in minutes"),
    db: Session = Depends(get_db)
):
    """
    Check for excessive ground time and create alerts.
    """
    new_alerts = alert_service.check_for_excessive_ground_time(db, threshold_minutes)
    return {"message": f"Checked for excessive ground time. Created {len(new_alerts)} new alerts.", "alerts": new_alerts}

@router.post("/check/route-deviations")
def check_for_route_deviations(
    db: Session = Depends(get_db)
):
    """
    Check for route deviations and create alerts.
    """
    new_alerts = alert_service.check_for_route_deviations(db)
    return {"message": f"Checked for route deviations. Created {len(new_alerts)} new alerts.", "alerts": new_alerts}
