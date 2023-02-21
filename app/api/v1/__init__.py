from fastapi import APIRouter

from .airports import airport_router

v1_router = APIRouter(prefix="/v1.0")

v1_router.include_router(airport_router)


@v1_router.get("/")
def index():
    return {"API status": "healthy"}
