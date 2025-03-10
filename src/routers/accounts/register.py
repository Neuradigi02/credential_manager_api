from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Request
import orjson
from src.services.captcha_service import verify_captcha, verify_recaptcha_v3
from src.services import accounts_service
from src.constants import VALIDATORS
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.accounts import register as register_data_access
from src.schemas.Accounts import Register
from src.utilities.aes_util import aes
from src.utilities.utils import data_frame_to_dict
from src.utilities.company_util import company_details
from src.core.load_config import config


router = APIRouter(
    tags=["Register"]
)


@router.post('/register')
async def register(request: Register, background_tasks: BackgroundTasks, req: Request):
    # print(request)
    if not config['IsDevelopment']:
        if company_details["is_captcha_system"]:
            is_valid, message = verify_captcha(encrypted_captcha_text=request.captchaData, captcha_reponse=request.captchaResponse)

            if not is_valid:
                return {'success': False, 'message': message}

        if company_details["is_recaptcha_v3"]:
            resp = await verify_recaptcha_v3(response_token=request.captchaResponse, action="Register", request=req)

            if not resp['success']:
                return {'success': False, 'message': resp['message']}

    is_email_verified = False

    if company_details["show_email_id"] and company_details["is_email_verification_before_registration"]:
        json_obj = orjson.loads(aes.decrypt(request.email_otp_enc))

        if json_obj['email_id'] != request.email:
            return {'success': False, 'message': 'Unable to verify email!'}
        
        elif float(json_obj['expire']) <= float(datetime.utcnow().timestamp()):
            return {'success': False, 'message': 'Email verification OTP expired!'}

        elif json_obj['otp'] != request.email_otp:
            return {'success': False, 'message': 'Invalid email verification OTP!'}

        else:
            is_email_verified = True

    is_mobile_verified = False

    if company_details["show_mobile_no"] and company_details["is_mobile_verification_before_registration"]:
        json_obj = orjson.loads(aes.decrypt(request.mobile_otp_enc))

        if json_obj['mobile_no'] != request.mobile:
            return {'success': False, 'message': 'Unable to verify mobile!'}
        
        elif float(json_obj['expire']) <= float(datetime.utcnow().timestamp()):
            return {'success': False, 'message': 'Mobile verification OTP expired!'}

        elif json_obj['otp'] != request.mobile_otp:
            return {'success': False, 'message': 'Invalid mobile verification OTP!'}

        else:
            is_mobile_verified = True

    dataset = await register_data_access.register(request, is_email_verified=is_email_verified, is_mobile_verified=is_mobile_verified)
    
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["success"]:
            df_user_info = dataset['rs_user_info']
            background_tasks.add_task(accounts_service.send_joining_mail_and_sms, df_user_info.iloc[0].loc["user_id"])
            
            return {'success': True, 'message': ds.iloc[0].loc["message"], 'user_info': data_frame_to_dict(df_user_info)}

        return {'success': False, 'message': ds.iloc[0].loc["message"]}
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


@router.get('/is_sponsor_valid')
async def is_sponsor_valid(sponsor_id: Annotated[str, VALIDATORS.USER_ID]):
    dataset = await register_data_access.is_sponsor_valid(sponsor_id=sponsor_id)

    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        ds = data_frame_to_dict(ds)
        return {'success': True, 'message': OK, 'data': ds }
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.get('/is_upline_valid')
async def is_upline_valid(upline_user_id: Annotated[str, VALIDATORS.USER_ID]):
    dataset = await register_data_access.is_upline_valid(upline_user_id=upline_user_id)

    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        ds = data_frame_to_dict(ds)
        return {'success': True, 'message': OK, 'data': ds }
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.get('/does_user_id_exist')
async def does_user_id_exist(user_id: Annotated[str, VALIDATORS.USER_ID]):
    dataset = await register_data_access.does_user_id_exist(user_id=user_id)

    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        ds = data_frame_to_dict(ds)
        return {'success': True, 'message': OK, 'data': ds }
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.get('/send_joining_mail_and_sms')
async def send_joining_mail_and_sms(id_enc: str):
    user_id = aes.decrypt(id_enc)
    return await accounts_service.send_joining_mail_and_sms(user_id=user_id)
