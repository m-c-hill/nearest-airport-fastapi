# Nearest Airport API

FastAPI app to return the nearest UK airport for a given coordinate. Coordinates are supplied as longitude and latitude in degrees to a `POST` endpoint, which calculates the distance to the nearest airport, as the crow flies, using the haversine formula.

## Getting Started

### Run the App

Create a `.env` in the root directory. Copy the contents of `.env-sample` into this file and set the `SECRET_KEY`.

The API can then be run in a Docker container by running the following:

```bash
docker compose up --build -d
```

The server can be accessed through [localhost:8008/api/v1.0](http://127.0.0.1:8008/api/v1.0/)

This command will start up three services:

- `fastapi-server-nearest-airport`: FastAPI application
- `postgres-nearest-airport`: Postgres server to host the backend database
- `redis-nearest-airport`: Redis server for temporarily caching requests

### Run the Tests

All tests can be found in the `tests` directory.

With the containers running, execute:

```bash
docker exec -it fastapi-server-nearest-airport /bin/bash ./run_tests.sh
```

Example output:

```bash
================================ test session starts ================================
platform linux -- Python 3.10.6, pytest-7.2.1, pluggy-1.0.0
rootdir: /app
plugins: mock-3.10.0, anyio-3.6.2
collected 10 items

tests/integration/test_airports.py .....         [ 50%]
tests/unit/test_services.py ....                 [100%]

=========================== 9 passed, 1 skipped in 0.23 ===========================
```

## Development

To assist future developers working on the project, below outlines the overall structure of the application and the key dependencies.

### Project Structure

```
.
└── nearest-airport-fastapi/
    ├── app/
    │   ├── api/
    │   │   ├── v1/
    │   │   │   ├── __init__.py
    │   │   │   └── airports.py
    │   │   └── __init__.py
    │   ├── core/
    │   │   ├── data/
    │   │   │   └── uk_airport_coords.csv
    │   │   ├── crud.py
    │   │   ├── database.py
    │   │   ├── models.py
    │   │   ├── schemas.py
    │   │   └── services.py
    │   ├── config.py
    │   ├── extensions.py
    │   └── main.py
    ├── tests/
    │   ├── data/
    │   │   ├── test_nearest_airport.db
    │   │   └── uk_airports_coords_test_data.csv
    │   ├── integration/
    │   │   └── test_airports.py
    │   ├── unit/
    │   │   └── test_services.py
    │   └── conftest.py
    ├── .env
    ├── .dockerignore
    ├── docker-compose.yml
    ├── Dockerfile
    ├── README.md
    ├── requirements.txt
    └── run_tests.sh
```

`main.py` - Server file to initialise the FastAPI app using the app factory function.

`app/api/__init__.py` - FastAPI app factory for creating and configuring a FastAPI app.

`config.py` - Configuration class for the app, with settings retrieved from environment variables, set using the .env file in the root directory.

`extensions.py` - FastAPI extensions, with database session generator and redis initialisation.

`airports.py` - Airport endpoints for the airports router, enabling requests to retrieve airport information and find the nearest airport to a point.

`crud.py` - CRUD functionality for interacting with the application's database.

`database.py` - Initialise the application's database. Development environment connects to a Postgres server, while a testing environment will create a local SQLite database in the tests/data directory.

`models.py` - ORM layer with SQLAlchemy models, representing tables in the application's database.

`schemas.py` - Pydantic schemas, used to model airport, coordinate and response objects, and to validate post bodies.

`services.py` - Service layer for the API with business logic used to manipulate a Pandas dataframe containing UK Airport information and return the nearest airport to an input coordinate.

### Key Dependencies

- [FastAPI](https://fastapi.tiangolo.com/) is a modern, high-performance web framework for building APIs. It emphasizes speed, ease of use, and developer productivity, leveraging modern Python features such as type annotations and async/await syntax. FastAPI is required to handle requests and responses for the nearest airport REST API.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the ORM (Object-relatonal mapping) library of choice, used to define the domain models and handle all database interactions.

- [PostgreSQL](https://www.postgresql.org/) is a database management system, providing a powerful and scalable solution for storing, retrieving, and managing structured data. It is used as the database for the development and production environment.

- [SQLite](https://www.sqlite.org/index.html) is a lightweight, open-source, serverless, self-contained, and cross-platform relational database management system that is embedded within applications and used for local data storage and processing. It is used as the database for the testing environment.

- [Pydantic](https://docs.pydantic.dev/) is used for data validation and settings management using Python type annotations.

- [Redis](https://redis.io/) is an open-source, in-memory data structure store, used in this project for caching some requests. [fakeredis](https://pypi.org/project/fakeredis/) is used to mock the redis server in the testing environment.

- [Pytest](https://docs.pytest.org/en/7.1.x/contents.html) was used as the testing framework for this project (using TDD), with unit and integration tests written to test the services and routes of the app.

- [Pandas](https://pandas.pydata.org/) is data manipulation and analysis library that provides data structures for efficiently storing and querying large datasets. It was used to calculate the distances between points on the Earth using the haversine formula.

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

## Theory

### Haversine Formula

\# TODO

## Future Improvements

\# TODO

- see linkedin message
- ...
- ...

## References

\# TODO

https://geodesy.geology.ohio-state.edu/course/refpapers/00740128.pdf
