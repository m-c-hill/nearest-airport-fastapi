"""
CRUD functionality for interacting with the application's database.
"""

import pathlib

import pandas as pd
from sqlalchemy.orm import Session

from app.core import models


def get_all_airports(db: Session) -> list[models.Airport]:
    return db.query(models.Airport).all()


def get_all_airports_df(db: Session) -> pd.DataFrame:
    return pd.read_sql_table("airports", db.get_bind())


def get_airport_by_id(id: int, db: Session) -> models.Airport | None:
    return db.query(models.Airport).filter_by(id=id).one_or_none()


def get_airport_by_icao(icao: str, db: Session) -> models.Airport | None:
    return db.query(models.Airport).filter_by(icao=icao).one_or_none()


def insert_airport_data(db: Session) -> None:
    filepath = f"{pathlib.Path(__file__).parent.resolve()}/data/uk_airport_coords.csv"
    df = _retrieve_airport_data_from_file(filepath)
    df.to_sql(
        "airports", db.get_bind(), if_exists="append", method="multi", index=False
    )


def _retrieve_airport_data_from_file(airport_data_filepath: str) -> pd.DataFrame:
    return pd.read_csv(airport_data_filepath).rename(
        columns={
            "NAME": "name",
            "ICAO": "icao",
            "Longitude": "longitude",
            "Latitude": "latitude",
        }
    )
