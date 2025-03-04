from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from ..services.competitor_service import get_competitor_analytics, get_competitor_flights, get_competitor_stats
from ..config.db import get_db
from ..models.competitor import CompetitorFlight

router = APIRouter(
    prefix="/api/competitors",
    tags=["competitors"],
)

@router.get("/analytics")
def competitor_analytics(db: Session = Depends(get_db)):
    """
    Retrieve competitor analytics data.
    """
    try:
        analytics = get_competitor_analytics(db)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/flights")
def get_flights(
    date_str: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """
    Retrieve competitor flights for a specific date.
    If no date is provided, returns today's flights.
    """
    try:
        if date_str:
            query_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            query_date = date.today()
            
        flights = get_competitor_flights(db, query_date)
        return {"flights": flights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
def get_stats(
    date_str: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """
    Retrieve competitor statistics for a specific date.
    If no date is provided, returns today's statistics.
    """
    try:
        if date_str:
            query_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            query_date = date.today()
            
        stats = get_competitor_stats(db, query_date)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
