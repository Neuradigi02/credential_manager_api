
from src.utilities.app_utils import get_sms_template, send_sms


async def send_joining_sms(user_id, user_name, mobile_no):
    context =   {
                    'user_id':user_id,
                    'user_name':user_name
                }

    template_id, message = await get_sms_template("joining_sms", context=context)

    return await send_sms(mobile_no=mobile_no, message=message, template_id=template_id)


async def send_two_factor_auth_otp_sms(user_id, user_name, mobile_no, otp):
    context =   {
                    'user_id':user_id,
                    'user_name':user_name,
                    'otp':otp
                }
    template_id, message = await get_sms_template("two_factor_auth_otp", context=context)

    return await send_sms(mobile_no=mobile_no, message=message, template_id=template_id)


async def send_reset_password_link_sms(user_id, user_name, mobile_no, reset_link):
    context =   {
                    'user_id':user_id,
                    'user_name':user_name,
                    'reset_link':reset_link
                }
    template_id, message = await get_sms_template("password_reset_link", context=context)
    
    return await send_sms(mobile_no=mobile_no, message=message, template_id=template_id)


async def send_contact_verification_otp_sms(user_id, user_name, mobile_no, otp):
    context =   {
                    'user_id':user_id,
                    'user_name':user_name,
                    'otp':otp
                }
    template_id, message = await get_sms_template("verification_otp", context=context)
   
    return await send_sms(mobile_no=mobile_no, message=message, template_id=template_id)


async def send_contact_verification_otp_sms_before_registration(mobile_no, otp):
    context =   {
                    'otp':otp
                }
    template_id, message = await get_sms_template("verification_otp_before_registration", context=context)
   
    return await send_sms(mobile_no=mobile_no, message=message, template_id=template_id)


async def send_topup_sms(user_id, user_name, mobile_no, package_name):
    context =   {
                    'user_id':user_id,
                    'user_name':user_name,
                    'package_name':package_name
                }
    template_id, message = await get_sms_template("topup_success", context=context)
   
    return await send_sms(mobile_no=mobile_no, message=message, template_id=template_id)


async def send_withdrawal_successful_sms(user_id, user_name, mobile_no, amount):
    context =   {
                    'user_id':user_id,
                    'user_name':user_name,
                    'amount':amount
                }
    template_id, message = await get_sms_template("withdrawal_successful", context=context)
   
    return await send_sms(mobile_no=mobile_no, message=message, template_id=template_id)


async def send_withdrawal_rejected_sms(user_id, user_name, mobile_no, amount):
    context =   {
                    'user_id':user_id,
                    'user_name':user_name,
                    'amount':amount
                }
    template_id, message = await get_sms_template("withdrawal_rejected", context=context)

    return await send_sms(mobile_no=mobile_no, message=message, template_id=template_id)
