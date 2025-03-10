
from fastapi import APIRouter
from .news import router as news_router
from .popup import router as popup_router

router = APIRouter(
    prefix="/misc",
    tags=["Misc Settings"]
)

router.include_router(news_router)
router.include_router(popup_router)
