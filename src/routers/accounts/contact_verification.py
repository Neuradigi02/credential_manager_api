from datetime import datetime, timedelta
import random
from typing import Annotated
from fastapi import APIRouter
import orjson
from src.services.email_service import send_contact_verification_otp_mail, send_contact_verification_otp_mail_before_registration, send_email_verification_link_mail
from src.services.sms_service import send_contact_verification_otp_sms, send_contact_verification_otp_sms_before_registration
from src.constants import VALIDATORS
from src.constants.messages import DATABASE_CONNECTION_ERROR
from src.data_access.accounts import contact_verification as data_access
from src.schemas.Accounts import ContactVerificationOTP
from src.utilities.aes_util import aes
from src.utilities.app_utils import get_route_by_control_id
from src.utilities.company_util import company_details

router = APIRouter(
    tags=["Contact Verification"]
)


@router.get('/get_contact_verification_otp')
async def get_contact_verification_otp(user_id: Annotated[str, VALIDATORS.USER_ID], contact_type: Annotated[str, VALIDATORS.CONTACT_TYPE], email_id_or_mobile_no: Annotated[str, VALIDATORS.EMAIL_OR_MOBILE_NUMBER]):
    dataset = await data_access.getOTPForContactVerification(user_id=user_id, contact_type=contact_type,
                                                       email_id_or_mobile_no=email_id_or_mobile_no)

    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']

        if ds.iloc[0].loc['success']:
            otp = ds.iloc[0].loc['otp']

            if contact_type == 'Mobile':
                is_sms_sent, sent_message = await send_contact_verification_otp_sms(user_id=user_id,
                                                                                    user_name=ds.iloc[0].loc['user_name'],
                                                                                    mobile_no=email_id_or_mobile_no,
                                                                                    otp=otp)
                return {'success': is_sms_sent, 'message': sent_message}

            if contact_type == 'Email':
                is_email_sent, sent_message = await send_contact_verification_otp_mail(user_id=user_id,
                                                                                       user_name=ds.iloc[0].loc[
                                                                                           'user_name'],
                                                                                       email_id=email_id_or_mobile_no,
                                                                                       otp=otp)
                return {'success': is_email_sent, 'message': sent_message}

        return {'success': False, 'message': ds.iloc[0].loc['message']}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


@router.post('/submit_contact_verification_otp')
async def submit_contact_verification_otp(request: ContactVerificationOTP):
    dataset = await data_access.submitOTPForContactVerification(user_id=request.user_id,
                                                                contact_type=request.contact_type,
                                                                email_id_or_mobile_no=request.email_id_or_mobile_no,
                                                                otp=request.otp)

    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        
        if ds.iloc[0].loc['success']:
            return {'success': True, 'message': ds.iloc[0].loc['message']}

        return {'success': False, 'message': ds.iloc[0].loc['message']}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


@router.get('/get_email_verification_link')
async def get_email_verification_link(user_id: Annotated[str, VALIDATORS.USER_ID], email_id: Annotated[str, VALIDATORS.EMAIL_ID]):
    dataset = await data_access.getOTPForContactVerification(user_id=user_id, contact_type='Email',
                                                             email_id_or_mobile_no=email_id)

    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']

        if ds.iloc[0].loc['success']:
            otp = ds.iloc[0].loc['otp']

            d = {'user_id': user_id, 'contact_type': 'Email', 'email_id_or_mobile_no': email_id, 'otp': otp}
            d_str = orjson.dumps(d).decode("utf-8")
            d_str = aes.encrypt(d_str)

            path = get_route_by_control_id('email_verification_link')['url'][1:]

            verification_link = company_details['website'] + path + '/' + d_str

            is_email_sent, sent_message = await send_email_verification_link_mail(user_id=user_id,
                                                                                  user_name=ds.iloc[0].loc['user_name'],
                                                                                  verification_link=verification_link,
                                                                                  email_id=email_id)

            return {'success': is_email_sent,
                    'message': 'Verification link sent successfully!' if is_email_sent else sent_message}

        return {'success': False, 'message': ds.iloc[0].loc['message']}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


@router.get('/verify_email_from_link')
async def verify_email_from_link(data: str):
    data = aes.decrypt(data)
    data = orjson.loads(data)

    dataset = await data_access.submitOTPForContactVerification(user_id=data['user_id'],
                                                                contact_type=data['contact_type'],
                                                                email_id_or_mobile_no=data['email_id_or_mobile_no'],
                                                                otp=data['otp'])

    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        
        if ds.iloc[0].loc['success']:
            return {'success': True, 'message': 'Email verified successfully!'}

        return {'success': False, 'message': 'Invalid or expired verification link!'}

    return {'success': False, 'message': 'Invalid or expired verification link!'}


@router.get('/get_email_verification_otp')
async def get_email_verification_otp(email_id: str):
    otp = str(random.randint(10000, 99999))
    is_email_sent, sent_message = await send_contact_verification_otp_mail_before_registration(email_id=email_id,
                                                                                               otp=otp)
    
    expire = (datetime.utcnow() + timedelta(minutes=float(company_details['otp_validity_minutes']))).timestamp()

    obj = {'email_id': email_id, 'expire': expire, 'otp': otp}

    obj_str = orjson.dumps(obj).decode("utf-8")

    if is_email_sent:
        return {'success': is_email_sent, 'message': sent_message, 'data': aes.encrypt(obj_str)}
    else:
        return {'success': is_email_sent, 'message': sent_message}


@router.get('/get_mobile_verification_otp')
async def get_mobile_verification_otp(mobile_no: str):
    otp = str(random.randint(10000, 99999))
    is_email_sent, sent_message = await send_contact_verification_otp_sms_before_registration(mobile_no=mobile_no, otp=otp)
    
    expire = (datetime.utcnow() + timedelta(minutes=float(company_details['otp_validity_minutes']))).timestamp()

    obj = {'mobile_no': mobile_no, 'expire': expire, 'otp': otp}

    obj_str = orjson.dumps(obj).decode("utf-8")

    if is_email_sent:
        return {'success': is_email_sent, 'message': sent_message, 'data': aes.encrypt(obj_str)}
    else:
        return {'success': is_email_sent, 'message': sent_message}
