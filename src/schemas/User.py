
from typing import Annotated
from pydantic import BaseModel
from src.constants import VALIDATORS


class UserPersonalDetailsUpdateRequest(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    name: Annotated[str, VALIDATORS.NAME] = ''
    dob: Annotated[str, VALIDATORS.REQUIRED]
    gender: Annotated[str, VALIDATORS.GENDER] = 'M'
    marital_status: Annotated[str, VALIDATORS.MARITAL_STATUS] = 'S'
    
class UserContactDetailsUpdateRequest(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    email_id: Annotated[str, VALIDATORS.EMAIL_ID] = ''
    mobile_no: Annotated[str, VALIDATORS.MOBILE_NO] = ''
    address: Annotated[str, VALIDATORS.DEFAULT] = ''
    district: Annotated[str, VALIDATORS.DEFAULT] = ''
    pin_code: str = ''
    country: int
    state: int
    two_factor_auth_request_id: str = ''
    
class UserNomineeDetailsUpdateRequest(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    nominee_title: Annotated[str, VALIDATORS.TITLE] = 'Mr'
    nominee_name: Annotated[str, VALIDATORS.NAME] = ''
    nominee_relationship: Annotated[str, VALIDATORS.NOMINEE_RELATIONSHIP]
    