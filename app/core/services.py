from math import asin, cos, sin, sqrt

import numpy as np
import pandas as pd
from numpy import deg2rad
from sklearn.neighbors import BallTree

from app.core.schemas import Airport, Coordinates

RADIUS_EARTH_KM = 6371

# =======================================
#  Nearest airport- brute force approach
# =======================================


def find_nearest_airport(
    airports: pd.DataFrame, coordinates: Coordinates
) -> tuple[Airport, float]:
    """
    Return the geospatially nearest airport to a pair of input coordinates from a dataset containing
    airport locations.
    """
    _convert_degrees_to_radians(airports)
    _add_haversine_distance(
        airports, coordinates.longitude_radians, coordinates.latitude_radians
    )

    nearest_airport_index = airports["distance_to_point"].idxmin()
    nearest_airport = airports.iloc[nearest_airport_index]

    return (
        Airport(**nearest_airport.to_dict()),
        nearest_airport.distance_to_point,
    )


def _convert_degrees_to_radians(airports: pd.DataFrame) -> None:
    """
    Add two new columns to the airports dataset with the longitude and latitude in radians
    """
    airports["latitude_radians"] = deg2rad(airports["latitude"])
    airports["longitude_radians"] = deg2rad(airports["longitude"])


def _add_haversine_distance(
    airports: pd.DataFrame,
    longitude: float,
    latitude: float,
) -> None:
    """
    Add a column to the airports dataframe with the distance from each airport to the input coordinates using
    the haversine formula
    """
    airports["distance_to_point"] = airports.apply(
        lambda df: _calculate_haversine_distance(
            df["longitude_radians"], df["latitude_radians"], longitude, latitude
        ),
        axis=1,
    )


def _calculate_haversine_distance(
    lon1: float, lat1: float, lon2: float, lat2: float
) -> float:
    """
    Calculate the great-circle distance in kilometres between two points on the earth (radians) using the
    haversine formula.
    """
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * RADIUS_EARTH_KM * asin(sqrt(a))


# =======================================
#  Nearest airport- ball tree approach
# =======================================


# TODO: not yet implemented correctly
def find_nearest_airport_balltree(airports: pd.DataFrame, coordinates: Coordinates):
    airport_locations = airports[["latitude", "longitude"]].values
    airport_locations_radians = deg2rad(airport_locations)
    tree = BallTree(airport_locations_radians, leaf_size=15, metric="haversine")
    random_geo = np.random.normal(
        loc=(coordinates.longitude_degrees, coordinates.latitude_degrees),
        scale=(0.1, 0.1),
        size=(10000, 2),
    )
    random_geo_radians = np.radians(random_geo)
    distances, idx = tree.query(random_geo_radians, k=1)

    nearest = airports.name[idx[:, 0]]
