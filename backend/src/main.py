from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import os
import asyncio

# Load environment variables
load_dotenv()

from .config.db import engine, Base
# Import all models to ensure they are registered with SQLAlchemy
from .models import flight, schedule, competitor, alert, aircraft
from .routers import flights, schedules, competitors, alerts, reports, websockets, flight_data
from .services.flight_update_service import update_flight_positions

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Air Ambulance Flight Tracker API",
    description="API for tracking air ambulance flights and comparing with competitors",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(flights.router)
app.include_router(schedules.router)
app.include_router(competitors.router)
app.include_router(alerts.router)
app.include_router(reports.router)
app.include_router(websockets.router)
app.include_router(flight_data.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Air Ambulance Flight Tracker API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Start background tasks
@app.on_event("startup")
async def startup_event():
    # Start the flight position update task
    asyncio.create_task(update_flight_positions())

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
