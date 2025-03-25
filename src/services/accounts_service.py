from src.core.logger import log_async, logger
from src.services.email_service import send_joining_mail
from src.core.security.Jwt import create_access_token
from src.schemas.TokenData import TokenData
from src.services.sms_service import send_joining_sms
from src.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_CREDENTIALS, INVALID_USER_ID, JOINING_INFO_ALREADY_SENT, JOINING_INFO_SEND_ERROR, UNKNOWN_ERROR
from src.data_access.accounts import login as data_access
from src.data_access.accounts import register as register_data_access
from src.data_access.user import details as user_details_data_access
from src.utilities.aes_util import aes
from src.utilities.app_utils import addCurrencySymbol, get_ip_info
from src.utilities.utils import get_real_client_ip, hide_email_address, hide_mobile_no, is_integer
from src.utilities.company_util import company_details
from src.core.load_config import config
from fastapi import BackgroundTasks, Request


async def member_id_to_user_id(member_id: str):
    try:
        if not is_integer(member_id):
            return member_id

        dataset = await data_access.get_user_id_from_member_id(member_id=int(member_id))

        if len(dataset) > 0 and len(dataset['rs']) > 0:
            if dataset['rs'].iloc[0].loc['success']:
                return dataset['rs'].iloc[0].loc['user_id']
        return member_id
    except Exception as e:
        return member_id


async def login(username: str, password: str, request: Request, background_tasks: BackgroundTasks, by_admin_user_id: str=''):
    url = dict(request.scope["headers"]).get(b"referer", b"").decode()  # request.base_url.__str__()

    client_ip_address = get_real_client_ip(request)

    ip_details = await get_ip_info(client_ip_address)

    dataset = await data_access.login(user_id=username,
                                      password=password,
                                      url=url,
                                      host=client_ip_address,
                                      ip_details=ip_details,
                                      by_admin_user_id=by_admin_user_id)

    if len(dataset) > 0:
        login_info_df = dataset['rs']
        if len(login_info_df) > 0:
            if login_info_df.iloc[0].loc['valid']:  # credentials are valid
                return await request_login_token(user_id=login_info_df.iloc[0].loc['user_id'],
                                                 login_id=int(login_info_df.iloc[0].loc['login_id']),
                                                 background_tasks=background_tasks)

            return {'success': False, 'message': INVALID_CREDENTIALS}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


async def request_login_token(user_id: str, login_id: int, background_tasks: BackgroundTasks):
    # login_id = aes.decrypt(login_id)
    dataset = await data_access.can_get_login_token(user_id=user_id, login_id=login_id)

    if len(dataset) > 0:

        login_info_df = dataset['rs']

        if len(login_info_df) > 0:
            if login_info_df.iloc[0].loc['valid']:  # login_id is valid

                http_access_token = ""
                ws_access_token = ""
                if login_info_df.iloc[0].loc['can_get_token']:  # is eligible to get login token
                    payload = TokenData()
                    payload.user_id = login_info_df.iloc[0].loc['user_id']
                    payload.role = login_info_df.iloc[0].loc['user_type']
                    payload.access_rights = login_info_df.iloc[0].loc['access_rights']
                    payload.token_id = int(login_info_df.iloc[0].loc['token_id'])

                    http_access_token = create_access_token(data={"payload": payload.dict()})

                    payload.token_type = "WEBSOCKET"
                    ws_access_token = create_access_token(data={"payload": payload.dict()})

                    if login_info_df.iloc[0].loc['user_type'] == 'User':
                        background_tasks.add_task(send_joining_mail_and_sms, user_id)
                        # await send_joining_mail_and_sms(user_id)

                two_factor_auth_request_id = ""
                if login_info_df.iloc[0].loc["is_two_factor_auth_enabled"] and login_info_df.iloc[0].loc['two_factor_auth_request_id'] > 0:
                    two_factor_auth_request_id = aes.encrypt(str(login_info_df.iloc[0].loc['two_factor_auth_request_id']))

                return {
                    'success': True,
                    'message': login_info_df.iloc[0].loc['message'],
                    'data': {
                        'token': http_access_token,
                        'ws_token': ws_access_token,
                        'can_get_token': bool(login_info_df.iloc[0].loc['can_get_token']),
                        'code': int(login_info_df.iloc[0].loc['code']),
                        'user_id': login_info_df.iloc[0].loc['user_id'],
                        'user_type': login_info_df.iloc[0].loc['user_type'],
                        'access_rights': login_info_df.iloc[0].loc['access_rights'],
                        'profile_image_url': login_info_df.iloc[0].loc['profile_image_url'],
                        'is_two_factor_auth_enabled': bool(login_info_df.iloc[0].loc['is_two_factor_auth_enabled']),
                        'is_two_factor_auth_successful': bool(login_info_df.iloc[0].loc['is_two_factor_auth_successful']),
                        'two_factor_auth_request_id': two_factor_auth_request_id,
                        'is_email_verification_required': bool(login_info_df.iloc[0].loc['is_email_verification_required']),
                        'is_email_verified': bool(login_info_df.iloc[0].loc['is_email_verified']),
                        'is_mobile_verification_required': bool(login_info_df.iloc[0].loc['is_mobile_verification_required']),
                        'is_mobile_verified': bool(login_info_df.iloc[0].loc['is_mobile_verified']),
                        'email_id': login_info_df.iloc[0].loc['email_id'],
                        'mobile_no': login_info_df.iloc[0].loc['mobile_no'],
                        'login_id': aes.encrypt(str(login_id))
                    }}

            return {'success': False, 'message': login_info_df.iloc[0].loc['message']}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


async def send_joining_mail_and_sms(user_id: str):
    try:
        dataset = await user_details_data_access.get_user_details(user_id=user_id)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["valid"]:
                is_email_sent=False
                is_sms_sent=False

                if ds.iloc[0].loc["is_joining_mail_sent"] and ds.iloc[0].loc["is_joining_sms_sent"]:
                    return {'success': False, 'message': JOINING_INFO_ALREADY_SENT }

                email_id = ds.iloc[0].loc['email_id']
                if not ds.iloc[0].loc["is_joining_mail_sent"]:
                    is_email_sent, sent_message = await send_joining_mail(user_id=ds.iloc[0].loc['user_id'],
                                                                        user_name=ds.iloc[0].loc['name'],
                                                                        email_id=email_id,
                                                                        joining_amount=addCurrencySymbol(str(round(ds.iloc[0].loc['joining_amount'], int(company_details['round_off_digits'])))),
                                                                        sponsor_id=ds.iloc[0].loc['sponsor_id'],
                                                                        referral_link=ds.iloc[0].loc['referral_link'])

                mobile_no = ds.iloc[0].loc['mobile_no']
                if not ds.iloc[0].loc["is_joining_sms_sent"]:
                    is_sms_sent, sent_message = await send_joining_sms(user_id=ds.iloc[0].loc['user_id'], user_name=ds.iloc[0].loc['name'], mobile_no=mobile_no)

                await register_data_access.update_joining_mail_and_sms_status(user_id=user_id, is_email_sent=is_email_sent, is_sms_sent=is_sms_sent)

                if is_email_sent or is_sms_sent:
                    msg = "Your joining info is sent to your" + ((" mobile number" + hide_mobile_no(mobile_no=mobile_no)) if(is_sms_sent) else "") + (" and " if(is_sms_sent and is_email_sent) else "") + (" email id "+ hide_email_address(email_id=email_id) if(is_sms_sent) else "") +"."
                    return {'success': True, 'message': msg }

                return {'success': False, 'message': JOINING_INFO_SEND_ERROR }

            return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        await log_async(logger.warning, e.__str__())
        return {'success': False, 'message':  UNKNOWN_ERROR}