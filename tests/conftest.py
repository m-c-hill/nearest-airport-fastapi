import os

from fastapi import FastAPI

os.environ["ENV"] = "testing"

import pytest

from app.api import create_app


@pytest.fixture(scope="session")
def app() -> FastAPI:
    yield create_app()
