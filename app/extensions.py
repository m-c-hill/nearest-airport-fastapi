from redis import Redis

from app.core.database import SessionLocal

rd = Redis(host="redis", port=6379, db=0)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# TODO
def register_exception_handlers():
    pass
