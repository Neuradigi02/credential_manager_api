
from fastapi import APIRouter

from .admin_profile import router as profile_router
from .details import router as details_router
from .member_search import router as member_search_router
from .miscellaneous import router as misc_router
from .subadmin import router as subadmin_router

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

router.include_router(details_router)
router.include_router(profile_router)
router.include_router(member_search_router)
router.include_router(subadmin_router)
router.include_router(misc_router)