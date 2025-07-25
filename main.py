from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, date
from typing import Optional, List
import re
from api import all_routers
from validators import MethodValidator, DateSearchValidator, CityValidator



app = FastAPI()

for router in all_routers:
    app.include_router(router)
