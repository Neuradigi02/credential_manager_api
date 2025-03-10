
from fastapi import APIRouter

from .contact_us import router as contact_us_router
from .newsletter import router as newsletter_router
from .visitors import router as visitors_router

router = APIRouter(
    tags=["Home"]
)


router.include_router(contact_us_router)
router.include_router(newsletter_router)
router.include_router(visitors_router)