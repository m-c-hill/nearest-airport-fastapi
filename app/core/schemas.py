from numpy import deg2rad
from pydantic import BaseModel, Field

from app.core import models


class Response(BaseModel):
    success: bool


class Airport(BaseModel):
    id: int
    name: str
    icao: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True


class AirportResponse(Response):
    airport: Airport


class AirportsResponse(Response):
    airports: list[Airport]
    airport_count: int


class Coordinates(BaseModel):
    longitude_degrees: float = Field(..., le=180, ge=-180)
    latitude_degrees: float = Field(..., le=90, ge=-90)

    @property
    def longitude_radians(self) -> float:
        return deg2rad(self.longitude_degrees)

    @property
    def latitude_radians(self) -> float:
        return deg2rad(self.latitude_degrees)


class NearestAirportResponse(Response):
    airport: Airport
    distance_km: float
