
from typing import Annotated
from pydantic import BaseModel

from src.constants import VALIDATORS


class TwoFactorAuthenticationRequest(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    request_id: Annotated[str, VALIDATORS.TWO_FACTOR_AUTH_REQUEST_ID]
    mode: Annotated[str, VALIDATORS.TWO_FACTOR_AUTH_MODE]
    code: Annotated[str, VALIDATORS.OTP]
    

class ChangePassword(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    user_type: Annotated[str, VALIDATORS.USER_TYPE]
    old_password: Annotated[str, VALIDATORS.PASSWORD]
    new_password: Annotated[str, VALIDATORS.PASSWORD]
    two_factor_auth_request_id: str = ''


class ChangePasswordByAdmin(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    new_password: Annotated[str, VALIDATORS.PASSWORD]


class SetupAuthenticatorApp(BaseModel):
    key: str
    verification_code: int
