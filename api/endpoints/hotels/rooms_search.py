from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from exceptions import CityValidationException, DateSearchValidationException, MethodValidationException
from typing import Optional, List
from services import HotelRoomService

app = APIRouter()

@app.api_route("/get_rooms", methods=['GET'])
async def get_rooms(request: Request, hotel_id: int, check_in: Optional[str] = None, check_out: Optional[str] = None):
    current_method: str = request.method
    correct_method: str = "GET"
    service =  HotelRoomService(hotel_id, check_in, check_out)
    rooms = service.get_rooms()

    return JSONResponse(
        content={
            "status": "ok",
            "code": 0,
            "data": {
                "rooms": [room.to_dict() for room in rooms],
            }
        }
    )