"""
Airport routes for the airports router. Routes include:
    - GET /api/v1/airports
    - GET /api/v1/airports/<id:int>
    - GET /api/v1/airports/icao/<icao_id:string>
    - POST /api/v1/airports/nearest
"""

import pickle

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import crud, schemas
from app.core.services import find_nearest_airport
from app.extensions import get_db, rd

airport_router = APIRouter(prefix="/airports", tags=["airports"])


@airport_router.get("/", response_model=schemas.AirportsResponse)
async def get_airports(db: Session = Depends(get_db)):
    """
    Return a list of all airports currently stored in the 'airports' table
    """
    airports = crud.get_all_airports(db)

    if not airports:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Airport data has not loaded into database correctly",
        )

    return schemas.AirportsResponse(
        success=True, airports=airports, airport_count=len(airports)
    )


@airport_router.get("/{airport_id}", response_model=schemas.AirportResponse)
async def get_airport_by_id(airport_id: int, db: Session = Depends(get_db)):
    """
    Return an airport for a given ID
    """
    airport = crud.get_airport_by_id(airport_id, db)

    if not airport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Airport with id {airport_id} cannot be found",
        )

    return schemas.AirportResponse(success=True, airport=airport)


@airport_router.get("/icao/{icao}", response_model=schemas.AirportResponse)
async def get_airport_by_icao(icao: str, db: Session = Depends(get_db)):
    """
    Return an airport for a given ICAO aiport code
    """
    airport = crud.get_airport_by_icao(icao.upper(), db)

    if not airport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Airport with ICAO code {icao.upper()} cannot be found",
        )

    return schemas.AirportResponse(success=True, airport=airport)


@airport_router.post("/nearest", response_model=schemas.NearestAirportResponse)
async def nearest_airport(
    coordinates: schemas.Coordinates, db: Session = Depends(get_db)
):
    """
    Return the nearest airport to a coordinate, defined in the post body
    """
    # Validation of input coordinates handled by pydantic (see Coordinates in schemas.py)

    coordinates_hash = hash(tuple(coordinates))
    if rd.get(coordinates_hash):
        nearest_airport, distance_km = pickle.loads(rd.get(coordinates_hash))
        return schemas.NearestAirportResponse(
            success=True, nearest_airport=nearest_airport, distance=distance_km
        )

    airports_df = crud.get_all_airports_df(db)
    nearest_airport, distance_km = find_nearest_airport(airports_df, coordinates)

    five_minutes = 5 * 60
    rd.set(
        coordinates_hash, pickle.dumps((nearest_airport, distance_km)), ex=five_minutes
    )

    return schemas.NearestAirportResponse(
        success=True,
        nearest_airport=nearest_airport,
        distance_km=distance_km,
        input_coordinates=coordinates,
    )
