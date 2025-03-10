
from fastapi import APIRouter

from .details import router as details_router
from .kyc import router as kyc_router
from .payment_info import router as payment_info_router
from .profile import router as profile_router

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

router.include_router(details_router)
router.include_router(profile_router)
router.include_router(payment_info_router)
router.include_router(kyc_router)