
from typing import Annotated
from pydantic import BaseModel
from src.utilities.company_util import company_details
from src.constants import VALIDATORS


class Register(BaseModel):
    referralId: str = ''
    userId: Annotated[str, VALIDATORS.USER_ID] = ''

    if not company_details['is_decentralized']:
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

        mobile: Annotated[str, VALIDATORS.MOBILE_NO] = ''
        mobile_otp_enc: str = ''
        mobile_otp: str = ''

        email: Annotated[str, VALIDATORS.EMAIL_ID] = ''
        email_otp_enc: str = ''
        email_otp: str = ''

    if company_details['is_pin_paid_registration']:
        pinNumber: int = 0
        pinPassword: int = 0

    if company_details['is_binary_system']:
        side: Annotated[str, VALIDATORS.SIDE] = 'L'

        # if(company_details['is_upline_registration']):
        uplineId: Annotated[str, VALIDATORS.USER_ID] = ''

    if company_details['is_nominee_registration']:
        nomineeTitle: Annotated[str, VALIDATORS.TITLE] = 'Mr'
        nomineeName: Annotated[str, VALIDATORS.NAME]
        nomineeRelationship: Annotated[str, VALIDATORS.NOMINEE_RELATIONSHIP]

    if company_details['is_bank_info_registration']:
        bankName: str = ''
        branchName: str = ''
        IFSCode: Annotated[str, VALIDATORS.IFSCODE] 
        bankAccountNumber: Annotated[str, VALIDATORS.BANK_ACCOUNT_NUMBER]
        accountHolderName: Annotated[str, VALIDATORS.NAME]
        aadharCardNumber: Annotated[str, VALIDATORS.AADHAAR_CARD_NUMBER] = ''
        aadharName: Annotated[str, VALIDATORS.NAME] = ''
        aadharImageFront: str = ''
        aadharImageBack: str = ''
        profileImage: str = ''
        panCardNumber: Annotated[str, VALIDATORS.PAN_CARD_NUMBER]
        panCardName: Annotated[str, VALIDATORS.NAME] = ''
        panCardImage: str = ''

    captchaData: str = ''
    captchaResponse: str = ''


class LoginRequest(BaseModel):
    username: Annotated[str,  VALIDATORS.USER_ID if not company_details['is_decentralized'] else VALIDATORS.USER_ID_DAPP] = ''  
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

