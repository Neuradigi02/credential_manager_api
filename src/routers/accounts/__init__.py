
from fastapi import APIRouter

from .contact_verification import router as contact_verification_router
from .forgot_password import router as forgot_password_router
from .login import router as login_router
from .register import router as register_router
from .captcha import router as captcha_router

router = APIRouter(
    prefix="/accounts"
)

router.include_router(login_router)
router.include_router(register_router)
router.include_router(forgot_password_router)
router.include_router(contact_verification_router)
router.include_router(captcha_router)
