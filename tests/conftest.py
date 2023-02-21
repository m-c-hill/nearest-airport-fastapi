import os

from fastapi import FastAPI

os.environ["ENV"] = "testing"

import fakeredis
import pytest

from app.api import create_app


@pytest.fixture(scope="session")
def app() -> FastAPI:
    yield create_app()


@pytest.fixture(scope="function")
def redis_mock():
    yield fakeredis.FakeStrictRedis(version=6)
