
from fastapi import APIRouter

from .routes import router as routes_router

router = APIRouter(
    prefix="/setup",
    tags=["Setup"]
)

router.include_router(routes_router)
