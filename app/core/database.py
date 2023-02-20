"""
Initialise the application's database. Development environment connects to a Postgres server, while
a testing environment will create a local SQLite database in the tests/data directory.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

if settings.environment == "testing":
    engine = create_engine(
        settings.test_db_url, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(settings.db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
