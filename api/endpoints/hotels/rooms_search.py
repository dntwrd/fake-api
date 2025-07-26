from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from exceptions import CityValidationException, DateSearchValidationException, MethodValidationException
from typing import Optional, List
from services import HotelSearchService

app = APIRouter()

@app.api_route("/get_rooms", methods=['GET'])
async def get_rooms(request: Request, hotel_id: int, check_in: Optional[str] = None, check_out: Optional[str] = None):
    return JSONResponse(
        content={
            "status": "ok",
            "code": 0,
            "data": {
                "hotel_id": hotel_id,
            }
        }
    )