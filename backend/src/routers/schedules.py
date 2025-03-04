from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, date
from ..services.schedule_service import get_schedules_by_date, compare_schedules_with_flights
from ..config.db import get_db

router = APIRouter(
    prefix="/api/schedules",
    tags=["schedules"],
)

@router.get("/")
def get_schedules(
    date_str: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """
    Retrieve schedules for a specific date.
    If no date is provided, returns today's schedules.
    """
    try:
        if date_str:
            query_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            query_date = date.today()
            
        schedules = get_schedules_by_date(db, query_date)
        return {"schedules": schedules}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/comparison")
def schedule_comparison(
    date_str: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """
    Compare scheduled flights with actual flights for a specific date.
    If no date is provided, returns today's comparison.
    """
    try:
        if date_str:
            query_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            query_date = date.today()
            
        comparison = compare_schedules_with_flights(db, query_date)
        return {"comparison": comparison}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 