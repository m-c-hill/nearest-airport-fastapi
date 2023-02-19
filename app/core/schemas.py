from pydantic import BaseModel


class Airport(BaseModel):
    name: str
    icao: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True
