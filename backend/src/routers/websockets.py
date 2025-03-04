from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import List
import asyncio

from ..config.db import get_db
from ..websockets.flight_socket import flight_manager
from ..services.flight_service import get_active_flights

router = APIRouter(
    prefix="/ws",
    tags=["websockets"],
)

@router.websocket("/flights")
async def websocket_flights(websocket: WebSocket, db: Session = Depends(get_db)):
    await flight_manager.connect(websocket)
    try:
        while True:
            # Wait for any message from the client (can be used as a heartbeat)
            await websocket.receive_text()
            
            # Get the latest flight data
            active_flights = get_active_flights(db)
            
            # Convert to dict for JSON serialization
            flight_data = {
                "flights": [
                    {
                        "id": flight.id,
                        "flight_id": flight.flight_id,
                        "tail_number": flight.tail_number,
                        "status": flight.status,
                        "departure_time": flight.departure_time.isoformat() if flight.departure_time else None,
                        "arrival_time": flight.arrival_time.isoformat() if flight.arrival_time else None,
                        "current_position_lat": flight.current_position_lat,
                        "current_position_lon": flight.current_position_lon,
                        "altitude": flight.altitude,
                        "speed": flight.speed,
                        "heading": flight.heading
                    }
                    for flight in active_flights
                ]
            }
            
            # Send the data to the client
            await websocket.send_json(flight_data)
            
            # Sleep for a short time to avoid overwhelming the database
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        flight_manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        flight_manager.disconnect(websocket) 