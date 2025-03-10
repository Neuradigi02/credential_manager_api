
from fastapi import APIRouter, BackgroundTasks, Request, Depends

from src.services import accounts_service
from src.services.captcha_service import verify_captcha, verify_recaptcha_v3
from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.schemas.Accounts import LoginRequest, LoginTokenRequest
from src.core.load_config import config
from src.utilities.company_util import company_details
from src.utilities.aes_util import aes

router = APIRouter(
    tags=["Login"]
)


@router.post('/login')
async def login(data: LoginRequest, request: Request, background_tasks: BackgroundTasks):
    if not config['IsDevelopment']:
        if company_details["is_captcha_system"]:
            is_valid, message = verify_captcha(encrypted_captcha_text=data.captcha_data, captcha_reponse=data.captcha_response)

            if not is_valid:
                return {'success': False, 'message': message}

        if company_details["is_recaptcha_v3"]:
            
            resp = await verify_recaptcha_v3(response_token=data.captcha_response, action="Login", request=request)

            if not resp['success']:
                return {'success': False, 'message': resp['message']}

    return await accounts_service.login(username=data.username, password=data.password, request=request, background_tasks=background_tasks)


@router.post('/login_through_admin', dependencies=[Depends(RightsChecker([26]))])
async def login(data: LoginRequest, request: Request, background_tasks: BackgroundTasks, token_payload: any = Depends(get_current_user)):
    return await accounts_service.login(username=data.username, password=data.password, request=request, background_tasks=background_tasks, by_admin_user_id=token_payload['user_id'])


@router.post('/request_login_token')
async def request_login_token(req: LoginTokenRequest, background_tasks: BackgroundTasks):
    login_id = int(aes.decrypt(req.login_id))
    return await accounts_service.request_login_token(user_id=req.user_id, login_id=login_id, background_tasks=background_tasks)
