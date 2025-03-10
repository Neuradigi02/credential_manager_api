
from fastapi import APIRouter

from src.routers.home import router as home_router
from src.routers.accounts import router as accounts_router
from src.routers.admin import router as admin_router
from src.routers.user import router as user_router
from src.routers.security import router as security_router
from src.routers.support import router as support_router
from src.routers.notifications import router as notifications_router
from src.routers.setup import router as setup_router
from src.routers import company, encrypt_decrypt_rsa, misc, encrypt_decrypt
from src.core.load_config import config


router = APIRouter()


router.include_router(home_router)
router.include_router(company.router)
router.include_router(accounts_router)
router.include_router(admin_router)
router.include_router(user_router)
router.include_router(security_router)
router.include_router(support_router)
router.include_router(notifications_router)
router.include_router(misc.router)

if config['IsDevelopment']:
    router.include_router(setup_router)
    router.include_router(encrypt_decrypt.router)
    router.include_router(encrypt_decrypt_rsa.router)

@router.get('/test')
def test():
    return 'Api is working properly'
