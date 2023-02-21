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
  "distance_km": 14.6968,
  "input_coordinates": {
    "longitude_degrees": 52,
    "latitude_degrees": -0.3
}
```

## Theory

### Haversine Formula

The haversine formula is a mathematical formula that is used to calculate the distance between two points on the surface of a sphere, such as the Earth [1]. It takes into account the curvature of the Earth and is particularly useful for determining distances between two points specified by their longitude and latitude coordinates.

The haversine formula is based on the law of haversines, states that the haversine between two points on a sphere, A and B, can be calculated as follows:

![haversine](<https://latex.codecogs.com/png.image?\dpi{200}hav(\theta)%20=%20hav(\Delta_{\phi})%20+%20\cos(\phi_1)\cos(\phi_2)hav(\Delta_{\lambda})>)

with:

![hav_theta](<https://latex.codecogs.com/png.image?\dpi{150}hav(\theta)%20=%20sin^{2}\left%20(%20\frac{x}{2}%20\right%20)>)

![](https://latex.codecogs.com/png.image?\dpi{150}\Delta_{\phi}%20=%20\phi_2%20-%20\phi_1)

![](https://latex.codecogs.com/png.image?\dpi{150}\Delta_{\lambda}%20=%20\lambda_2%20-%20\lambda_1)

and where:

`λ1, λ2` are the longitudes of points A and B, respectively,

`φ1, φ2` are the latitudes of points A and B, respectively,

`θ` is the central angle between the two points, A and B, on the sphere.

![haversine](https://images.prismic.io/sketchplanations/e1e45776-aa40-4806-820e-b5c5b8050f4b_SP+687+-+The+haversine+formula.png?auto=compress,format)

To calculate the distance between two points given their longitude and latitude coordinates in radians, the haversine formula can be rearranged as follows:

![haversine_distance](<https://latex.codecogs.com/svg.image?\dpi{150}d%20=%202r\sqrt{sin^2\left(\frac{\Delta_{\theta}}{2}\right)%20+%20\cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta_{\lambda}}{2}\right)}>)

where:

`d` is the distance between the two points in kilometers
`r` is the radius of the Earth (mean radius = 6,371km [2])

## Future Improvements

- Improve the algorithm used to find the nearest airport. The method currently uses a brute force approach to calculate the distance to each airport before selecting the airport with the smallest distance. This could potentially be improved by using a nearest neighbour search with [scikit-learn's balltree](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.BallTree.html). However, given the relatively small sample size of UK airports, it did not feel necessary to implement such a method.
- Implement an API throttler to rate limit endpoints by IP address using redis. A simple example can be found in the [following Medium article](https://sayanc20002.medium.com/api-throttling-using-redis-and-fastapi-dockerized-98a50f9495c).
- Add custom error handlers and add Pydantic response models to standardise the API's error responses.
- Invert database dependency with a repository layer between the models and the database.
- Update Swagger documentation with more informative descriptions.
- Implement a simple frontend which shows the user's location and their nearest airport on a map.

## References

[1] Upadhyay, A., 2019. _Haversine Formula – Calculate geographic distance on earth_ [Online]. IGISMAP. Available from: https://www.igismap.com/haversine-formula-calculate-geographic-distance-earth/ [Accessed 19 February 2023].

[2] Moritz, H. _Geodetic Reference System 1980_. Journal of Geodesy 74, 128–133 (2000). Available from: https://geodesy.geology.ohio-state.edu/course/refpapers/00740128.pdf [Accessed 19 February 2023].
