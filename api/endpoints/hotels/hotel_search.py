from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from exceptions import CityValidationException, DateSearchValidationException, MethodValidationException
from typing import Optional, List
from services import HotelSearchService

app = APIRouter()

@app.api_route("/search", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def search(request: Request, city: Optional[str] = None, check_in: Optional[str] = None, check_out: Optional[str] = None):

    try:
        current_method: str = request.method
        correct_method: str = "GET"
        service = HotelSearchService(city, check_in, check_out, current_method, correct_method)
        hotels = service.search()

        return JSONResponse(
            content={
                "status": "ok",
                "code": 0,
                "data": {
                    "hotels": [hotel.to_dict() for hotel in hotels]
                }
            }
        )
    except MethodValidationException as e:
        return JSONResponse(
            status_code=200,
            content={
                "status": "error",
                "code": e.code,
                "message": e.message
            }
        )
    except CityValidationException as e:
        return JSONResponse(
            status_code=200,
            content={
                "status": "error",
                "code": e.code,
                "message": e.message
            }
        )
    except DateSearchValidationException as e:
        return JSONResponse(
            status_code=200,
            content={
                "status": "error",
                "code": e.code,
                "message": e.message
            }
        )