
from typing import Annotated
from pydantic import BaseModel
from src.constants import VALIDATORS


class AdminDetailsUpdateRequest(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    email_id: Annotated[str, VALIDATORS.EMAIL_ID] = ''
    mobile_no: Annotated[str, VALIDATORS.MOBILE_NO]
    two_factor_auth_request_id: str = ''


class AddNewAdminRequest(BaseModel):
    admin_user_id: Annotated[str, VALIDATORS.USER_ID]
    password: Annotated[str, VALIDATORS.PASSWORD]
    email_id: Annotated[str, VALIDATORS.EMAIL_ID] = ''
    mobile_no: Annotated[str, VALIDATORS.MOBILE_NO]
    

class AdminAccessRightsUpdateRequest(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    access_rights: Annotated[str, VALIDATORS.ACCESS_RIGHTS]
