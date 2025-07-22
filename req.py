from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Query


app = FastAPI()


@app.get("/search")
async def search(city : str = ""):
    return JSONResponse(
        content={
            "status": "ok",
            "code":0,
            "data": {
                "hotels": [
                    {
                        "id": 1,
                        "hotel_name": "Azimut",
                        "description": "Best hotel",
                        "city": city,
                        "country": "Russia",
                        "stars": None,
                        "price": 1000
                    }
                ]
            }
        }
    )

@app.post("/create")
async def create(name : str = ""):
    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "name": name if name else "empty"
            }
        }
    )