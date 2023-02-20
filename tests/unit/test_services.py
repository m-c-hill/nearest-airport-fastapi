import pandas as pd
import pytest

from app.core import schemas, services

# ===============================
#  Service fixtures
# ===============================


@pytest.fixture(scope="module")
def airport_dataframe() -> pd.DataFrame:
    return pd.read_csv("tests/data/uk_airport_coords_test_data.csv")


@pytest.fixture(scope="module")
def point_a() -> schemas.Coordinates:
    return schemas.Coordinates(longitude_degrees=-0.116773, latitude_degrees=51.510357)


@pytest.fixture(scope="module")
def point_b() -> schemas.Coordinates:
    return schemas.Coordinates(longitude_degrees=-77.009003, latitude_degrees=38.889931)


@pytest.fixture(scope="module")
def expected_coordinates_radians() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "latitude_radians": [0.913551, 0.918543],
            "longitude_radians": [0.013490, -0.055036],
        }
    )


@pytest.fixture(scope="module")
def expected_nearest_airport() -> schemas.Airport:
    return schemas.Airport(
        id=1, name="HONINGTON", icao="EGXH", longitude=52.342611, latitude=0.772939
    )


# ===============================
#  Service tests
# ===============================


def test_find_nearest_airport(airport_dataframe, point_a, expected_nearest_airport):
    nearest_airport, distance = services.find_nearest_airport(
        airport_dataframe, point_a
    )

    assert distance == pytest.approx(110.84, 0.01)


def test_convert_degrees_to_radians(airport_dataframe):
    services._convert_degrees_to_radians(airport_dataframe)

    assert airport_dataframe.iloc[0].longitude_radians == pytest.approx(0.01349, 0.0001)
    assert airport_dataframe.iloc[0].latitude_radians == pytest.approx(0.91355, 0.0001)
    assert airport_dataframe.iloc[1].longitude_radians == pytest.approx(
        -0.05504, 0.0001
    )
    assert airport_dataframe.iloc[1].latitude_radians == pytest.approx(00.91854, 0.0001)


def test_add_haversine_distance(airport_dataframe, point_a):
    services._convert_degrees_to_radians(airport_dataframe)
    services._add_haversine_distance(
        airport_dataframe, point_a.longitude_radians, point_a.latitude_radians
    )

    assert airport_dataframe.iloc[0].distance_to_point == pytest.approx(110.84, 0.01)
    assert airport_dataframe.iloc[1].distance_to_point == pytest.approx(241.92, 0.01)


def test_calculate_haversine_distance(point_a, point_b):
    distance_km = services._calculate_haversine_distance(
        point_a.longitude_radians,
        point_a.latitude_radians,
        point_b.longitude_radians,
        point_b.latitude_radians,
    )

    assert distance_km == pytest.approx(5897.658, 0.001)


@pytest.mark.skip(reason="Not yet implemented")
def test_find_nearest_airport_balltree(airport_dataframe, point_a):
    services.find_nearest_airport_balltree(airport_dataframe, point_a)
