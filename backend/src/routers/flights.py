from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services.flight_service import get_active_flights
from ..config.db import get_db

router = APIRouter(
    prefix="/api/flights",
    tags=["flights"],
)

@router.get("/active")
def active_flights(db: Session = Depends(get_db)):
    """
    Retrieve active flight data.
    """
    try:
        flights = get_active_flights(db)
        return {"flights": flights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
