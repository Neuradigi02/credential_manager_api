
from typing import Annotated
from fastapi import APIRouter, Depends

from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants import VALIDATORS
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.user import payment_info as data_access
from src.schemas.UserPaymentInfo import UserBankDetailsUpdateRequest, UserCryptoWithdrawalAddressRequest, \
    UserUpiDetailsUpdateRequest
from src.utilities.utils import data_frame_to_dict

router = APIRouter(
    dependencies=[Depends(get_current_user), Depends(RightsChecker([14,19]))]
)

@router.put('/update_bank_details')
async def update_bank_details(req: UserBankDetailsUpdateRequest, token_payload:any = Depends(get_current_user)):
    user_id = token_payload["user_id"]
    user_type = token_payload["role"]

    is_by_admin = False
    admin_user_id = ''

    if(user_type=="User"):
        req.user_id = user_id
    else:
        is_by_admin = True
        admin_user_id = user_id

    dataset = await data_access.update_user_bank_details(user_id=req.user_id, bank_name=req.bank_name, branch_name=req.branch_name, ifscode=req.ifscode, bank_account_no=req.bank_account_no, account_holder_name=req.account_holder_name, is_by_admin=is_by_admin, by_admin_user_id=admin_user_id)
    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return {'success': True, 'message': ds.iloc[0].loc["message"] }
        
        return {'success': False, 'message': ds.iloc[0].loc["message"] }
    
    return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}


@router.put('/update_upi_details')
async def update_upi_details(req: UserUpiDetailsUpdateRequest, token_payload:any = Depends(get_current_user)):
    user_id = token_payload["user_id"]
    user_type = token_payload["role"]

    is_by_admin = False
    admin_user_id = ''

    if(user_type=="User"):
        req.user_id = user_id
    else:
        is_by_admin = True
        admin_user_id = user_id

    dataset = await data_access.update_user_upi_details(user_id=req.user_id, upi_id=req.upi_id, is_by_admin=is_by_admin, by_admin_user_id=admin_user_id)
    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return {'success': True, 'message': ds.iloc[0].loc["message"] }
        
        return {'success': False, 'message': ds.iloc[0].loc["message"] }
    
    return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}


@router.get('/get_crypto_withdrawal_address')
async def get_crypto_withdrawal_address(user_id: Annotated[str, VALIDATORS.USER_ID], crypto_id: Annotated[int , VALIDATORS.REQUIRED], token_payload = Depends(get_current_user)):
    user_type = token_payload["role"]

    if(user_type=="User"):
        user_id = token_payload["user_id"]
        
    dataset = await data_access.get_user_crypto_withdrawal_address(user_id=user_id, crypto_id=crypto_id)
    if len(dataset)>0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_dict(ds)}
        
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.post('/add_crypto_withdrawal_address')
async def add_crypto_withdrawal_address(req: UserCryptoWithdrawalAddressRequest, token_payload:any = Depends(get_current_user)):
    user_id = token_payload["user_id"]
    user_type = token_payload["role"]

    is_by_admin = False
    admin_user_id = ''

    if(user_type=="User"):
        req.user_id = user_id
    else:
        is_by_admin = True
        admin_user_id = user_id

    dataset = await data_access.add_user_crypto_withdrawal_address(user_id=req.user_id, crypto_id=req.crypto_id, address=req.address, is_by_admin=is_by_admin, by_admin_user_id=admin_user_id)
    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return {'success': True, 'message': ds.iloc[0].loc["message"] }
        
        return {'success': False, 'message': ds.iloc[0].loc["message"] }
    
    return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

