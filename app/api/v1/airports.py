# from core import crud, schemas, services
# from core.database import get_db
from fastapi import APIRouter  # , Depends, HTTPException, status

# from sqlalchemy.orm import Session

airport_router = APIRouter(prefix="/airports", tags=["airports"])


@airport_router.get("/")
async def get_airports():
    return {"airports": "list of airports"}


@airport_router.get("/<id:int>")
async def get_airport_by_id():
    return {"airports": "list of airports"}


@airport_router.get("/<icao:string>")
async def get_airport_by_icao():
    return {"airports": "list of airports"}


@airport_router.post("/nearest")
async def nearest_aiport():
    return {"airport": "gatwick"}
