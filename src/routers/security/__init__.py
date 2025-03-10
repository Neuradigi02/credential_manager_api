
from fastapi import APIRouter

from .change_password import router as change_pass
from .two_factor_auth import router as twoFA

router = APIRouter(
    prefix="/security"
)

router.include_router(twoFA)
router.include_router(change_pass)