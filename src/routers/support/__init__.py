
from fastapi import APIRouter

from .support import router as support_router

router = APIRouter(
    prefix="/support",
    tags=["Support"]
)

router.include_router(support_router)
