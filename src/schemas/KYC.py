from typing import Annotated
from pydantic import BaseModel

from src.constants import VALIDATORS


class KYCRequest(BaseModel):
    name: str
    date_of_birth: str
    aadhaar_number: str
    aadhaar_front_image: str
    aadhaar_back_image: str
    pan_number: str
    pan_image: str


class GetKYCRequest(BaseModel):
    user_id: str = ''
    date_from: str = ''
    date_to: str = ''
    status: str = 'All'
    page_index: int = 0
    page_size: int = 100


class KycRequestApproveRejectDataItem(BaseModel):
    RequestId: int
    Remarks: str = ''
    Status: Annotated[str, VALIDATORS.STATUS_APPROVED_REJECTED]
