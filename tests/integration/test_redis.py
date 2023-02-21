from fastapi.testclient import TestClient


def test_nearest_airport_redis_caching(mocker, redis_mock, capfd, app):
    """
    Confirm that a repeat identical post request to airports/nearest hits retrieves the
    result from the redis cache on the second request by checking log messages.
    """
    mocker.patch("app.api.v1.airports.rd", redis_mock)
    coordinates = {"latitude_degrees": 52.327640, "longitude_degrees": 0.851955}
    with TestClient(app) as client:
        response_one = client.post("/api/v1.0/airports/nearest", json=coordinates)
        assert response_one.status_code == 200

        response_two = client.post("/api/v1.0/airports/nearest", json=coordinates)
        assert response_two.status_code == 200

        # Capture output to check logging messages. The first request should log the message
        #   "Calculating nearest airport!", while the second identical request will print out
        #   "Cache hit!".
        out, _ = capfd.readouterr()
        assert out == "Calculating nearest airport!\nCache hit!\n"
