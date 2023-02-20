# Nearest Airport API

FastAPI app to TODO

## Getting Started

### Run the App

The API can be run in a Docker container by running the following:

```bash
docker compose up --build -d
```

The server can be accessed through [localhost:8008/api/v1.0](http://127.0.0.1:8008/api/v1.0/)

This command will start up three services:

- `fastapi-server-nearest-airport`: FastAPI application
- `postgres-nearest-airport`: Postgres server to host the backend database
- `redis-nearest-airport`: Redis server for temporarily caching requests

### Run the Tests

All tests can be found in the `tests` directory. To run the tests:

```
./run-tests.sh
```

Example output:

```bash
================================ test session starts ================================
platform linux -- Python 3.10.6, pytest-7.2.1, pluggy-1.0.0
rootdir: /home/matt/dev/nearest-airport-fastapi
plugins: mock-3.10.0, anyio-3.6.2
collected 10 items

tests/integration/test_airports.py .....         [ 50%]
tests/unit/test_services.py ....                 [100%]

=========================== 9 passed, 1 skipped in 0.23 ===========================
```


## API Documentation

The API uses [Swagger](https://swagger.io/) for its documentation framework, which can be accessed at [localhost:8008/docs](http://127.0.0.1:8008/docs)

### Endpoints

`GET /airports`: Retrieve a complete list of all UK airports and their locations.

`GET /airports/<id:int>`: Retrieve an airport by id.

`GET /airports/icao/<icao:string>`: Retrieve an airport by icao airport code.

`POST /airports/nearest`: Retrieve the airport nearest to a point by submitting coordinate data with the following structure:

```json
{
  "longitude_degrees": 0.05112,
  "latitude_degrees": 54.2011
}
```

### Example Requests

#### `GET /airports/1`

Request:

```bash
curl http://127.0.0.1:8008/api/v1.0/airports/1
```

Response:

```json
{
  "success": true,
  "airport": {
    "id": 1,
    "name": "HONINGTON",
    "icao": "EGXH",
    "latitude": 52.342611,
    "longitude": 0.772939
  }
}
```

#### `POST /airports/nearest`

Request:

```bash
curl http://127.0.0.1:8008/api/v1.0/airports/nearest -X POST -H "Content-Type: application/json" -d '{"longitude_degrees":52, "latitude_degrees": -0.3}'
```

Response:

```json
{
  "success": true,
  "nearest_airport": {
    "id": 11,
    "name": "LUTON",
    "icao": "EGGW",
    "latitude": 51.874722,
    "longitude": -0.368333
  },
  "distance_km": 14.6968
}
```

### Key Dependencies

- FastAPI
- Postgres and SQLAlchemy
- Redis and fakeredis
- Pandas
- Pytest

## Theory

### Haversine Formula

## Future Improvements

- see linkedin message
- ...
- ...

## References

https://geodesy.geology.ohio-state.edu/course/refpapers/00740128.pdf
