
from typing import Annotated
from pydantic import BaseModel
from src.utilities.company_util import company_details
from src.constants import VALIDATORS


class Register(BaseModel):
    referralId: str = ''
    userId: Annotated[str, VALIDATORS.USER_ID] = ''

    password: Annotated[str, VALIDATORS.PASSWORD] = ''
    confirmPassword: Annotated[str, VALIDATORS.PASSWORD] = ''

    name: Annotated[str, VALIDATORS.NAME] = '' 
    dob: str | None = None
    maritalStatus: Annotated[str, VALIDATORS.MARITAL_STATUS] = 'S' 
    gender: Annotated[str, VALIDATORS.GENDER] = 'M' 
    address: str = ''
    district: str = ''
    state: int = 0
    country: int = 0
    pincode: str = ''

    if company_details['show_mobile_no']:
        mobile: Annotated[str, VALIDATORS.MOBILE_NO] = ''
        mobile_otp_enc: str = ''
        mobile_otp: str = ''

    if company_details['show_email_id']:
        email: Annotated[str, VALIDATORS.EMAIL_ID] = ''
        email_otp_enc: str = ''
        email_otp: str = ''

    captchaData: str = ''
    captchaResponse: str = ''


class LoginRequest(BaseModel):
    username: Annotated[str,  VALIDATORS.USER_ID] = ''  
    password: Annotated[str, VALIDATORS.PASSWORD]
    captcha_data: str = ''
    captcha_response: str = ''

    
class ResetPassword(BaseModel):
    request_id_enc: Annotated[str, VALIDATORS.REQUIRED]
    new_password: Annotated[str, VALIDATORS.PASSWORD]

    
class ContactVerificationOTP(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    contact_type: Annotated[str, VALIDATORS.CONTACT_TYPE]
    email_id_or_mobile_no: Annotated[str, VALIDATORS.EMAIL_OR_MOBILE_NUMBER]
    otp: Annotated[str, VALIDATORS.OTP]


class LoginTokenRequest(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    login_id: Annotated[str, VALIDATORS.LOGIN_ID]

