import pytest
from fastapi.testclient import TestClient

# ========================
#  Airport fixtures
# ========================


@pytest.fixture(scope="module")
def honington_airport() -> dict:
    return {
        "id": 1,
        "name": "HONINGTON",
        "icao": "EGXH",
        "latitude": 52.342611,
        "longitude": 0.772939,
    }


@pytest.fixture(scope="module")
def heathrow_airport() -> dict:
    return {
        "id": 9,
        "name": "HEATHROW",
        "icao": "EGLL",
        "latitude": 51.4775,
        "longitude": -0.461389,
    }


@pytest.fixture(scope="module")
def invalid_coordinates_response() -> dict:
    return {
        "detail": [
            {
                "loc": ["body", "latitude_degrees"],
                "msg": "ensure this value is less than or equal to 90",
                "type": "value_error.number.not_le",
                "ctx": {"limit_value": 90},
            }
        ]
    }


# ========================
#  Endpoint tests
# ========================


def test_get_airports(app, honington_airport):
    with TestClient(app) as client:
        response = client.get(
            "/api/v1.0/airports",
        )
        response_json = response.json()

        assert response.status_code == 200
        assert response_json["success"] == True
        assert response_json["airport_count"] == 59
        assert response_json["airports"][0] == honington_airport


def test_get_airport_by_id(app, honington_airport):
    with TestClient(app) as client:
        response = client.get(
            "/api/v1.0/airports/1",
        )
        response_json = response.json()

        assert response.status_code == 200
        assert response_json["success"] == True
        assert response_json["airport"] == honington_airport


def test_get_airport_by_id(app, honington_airport):
    with TestClient(app) as client:
        response = client.get(
            "/api/v1.0/airports/icao/EGXH",
        )
        response_json = response.json()

        assert response.status_code == 200
        assert response_json["success"] == True
        assert response_json["airport"] == honington_airport


def test_nearest_airport_honington(mocker, redis_mock, app, honington_airport):
    mocker.patch("app.api.v1.airports.rd", redis_mock)
    coordinates = {"latitude_degrees": 52.327640, "longitude_degrees": 0.851955}
    with TestClient(app) as client:
        response = client.post("/api/v1.0/airports/nearest", json=coordinates)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json["success"] == True
        assert response_json["nearest_airport"] == honington_airport
        assert response_json["distance_km"] == pytest.approx(5.609, 0.01)
        assert response_json["input_coordinates"] == coordinates


def test_nearest_airport_heathrow(mocker, redis_mock, app, heathrow_airport):
    mocker.patch("app.api.v1.airports.rd", redis_mock)
    coordinates = {"latitude_degrees": 51.408314, "longitude_degrees": -0.301567}
    with TestClient(app) as client:
        response = client.post("/api/v1.0/airports/nearest", json=coordinates)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json["success"] == True
        assert response_json["nearest_airport"] == heathrow_airport
        assert response_json["distance_km"] == pytest.approx(13.486, 0.01)
        assert response_json["input_coordinates"] == coordinates


def test_nearest_airport_invalid_coordinates(
    mocker, redis_mock, app, invalid_coordinates_response
):
    mocker.patch("app.api.v1.airports.rd", redis_mock)
    invalid_coordinatees = {"latitude_degrees": 100, "longitude_degrees": -0.301567}
    with TestClient(app) as client:
        response = client.post("/api/v1.0/airports/nearest", json=invalid_coordinatees)
        response_json = response.json()

        assert response.status_code == 422
        assert response_json == invalid_coordinates_response
