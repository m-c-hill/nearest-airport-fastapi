from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core import models
from app.core.crud import insert_airport_data
from app.core.database import SessionLocal, engine

from .v1 import v1_router


def create_app():
    models.Base.metadata.create_all(bind=engine)

    app = FastAPI(title="nearest-airport")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(v1_router, prefix="/api")

    @app.on_event("startup")
    def startup_populate_db():
        """
        Check if airport table is populated. If not, execute query to insert UK airport data.
        """
        db = SessionLocal()
        airport = db.query(models.Airport).first()
        if not airport:
            insert_airport_data(db)

    return app
