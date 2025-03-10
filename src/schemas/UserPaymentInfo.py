from typing import Annotated
from pydantic import BaseModel
from src.constants import VALIDATORS


class UserBankDetailsUpdateRequest(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    bank_name: str
    branch_name: str
    ifscode: Annotated[str, VALIDATORS.IFSCODE]
    bank_account_no: Annotated[str, VALIDATORS.BANK_ACCOUNT_NUMBER]
    account_holder_name: Annotated[str, VALIDATORS.NAME] = ''

class UserUpiDetailsUpdateRequest(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    upi_id: Annotated[str, VALIDATORS.UPI_ID]
    
class UserCryptoWithdrawalAddressRequest(BaseModel):
    user_id: Annotated[str, VALIDATORS.USER_ID]
    crypto_id: Annotated[int , VALIDATORS.REQUIRED]
    address: Annotated[str, VALIDATORS.REQUIRED]
    