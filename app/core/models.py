from sqlalchemy import Column, Float, Integer, String

from .database import Base


class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    icao = Column(String, unique=True)
    latitude = Column(Float)
    longitude = Column(Float)
