
from fastapi import APIRouter, Depends

from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR
from src.data_access.security import change_password as data_access
from src.schemas.Security import ChangePassword, ChangePasswordByAdmin
from src.utilities.aes_util import aes

router = APIRouter(
    tags=["Change Password"]
)


@router.put('/change_self_password', dependencies=[Depends(RightsChecker([24, 25, 61]))])
async def change_self_password(request: ChangePassword, token_payload:any = Depends(get_current_user)):
    user_id = token_payload["user_id"]
    user_type = token_payload["role"]

    if(request.two_factor_auth_request_id!=''):
        request.two_factor_auth_request_id = int(aes.decrypt(request.two_factor_auth_request_id))
    else:
        request.two_factor_auth_request_id = 0
        
    dataset = await data_access.changePassword(user_id=user_id, user_type=user_type, old_password=request.old_password, new_password=request.new_password, is_by_admin=False, by_admin_user_id='', two_factor_auth_request_id=request.two_factor_auth_request_id)

    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']

        if(ds.iloc[0].loc["success"]):
            return { 'success': True, 'message': ds.iloc[0].loc["message"] }

        return { 'success': False, 'message': ds.iloc[0].loc["message"] }
        

    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.put('/change_admin_password', dependencies=[Depends(RightsChecker([20]))])
async def change_admin_password(request: ChangePasswordByAdmin, token_payload:any = Depends(get_current_user)):
    user_id = token_payload["user_id"]

    dataset = await data_access.changePassword(user_id=request.user_id, user_type='Admin', old_password='', new_password=request.new_password, is_by_admin=True, by_admin_user_id=user_id)

    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']

        if(ds.iloc[0].loc["success"]):
            return { 'success': True, 'message': ds.iloc[0].loc["message"] }

        return { 'success': False, 'message': ds.iloc[0].loc["message"] }
        

    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.put('/change_user_password', dependencies=[Depends(RightsChecker([26]))])
async def change_user_password(request: ChangePasswordByAdmin, token_payload:any = Depends(get_current_user)):
    user_id = token_payload["user_id"]

    dataset = await data_access.changePassword(user_id=request.user_id, user_type='User', old_password='', new_password=request.new_password, is_by_admin=True, by_admin_user_id=user_id)

    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']

        if(ds.iloc[0].loc["success"]):
            return { 'success': True, 'message': ds.iloc[0].loc["message"] }

        return { 'success': False, 'message': ds.iloc[0].loc["message"] }
        

    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.put('/change_franchise_password', dependencies=[Depends(RightsChecker([180]))])
async def change_franchise_password(request: ChangePasswordByAdmin, token_payload:any = Depends(get_current_user)):
    user_id = token_payload["user_id"]

    dataset = await data_access.changePassword(user_id=request.user_id, user_type='Franchise', old_password='', new_password=request.new_password, is_by_admin=True, by_admin_user_id=user_id)

    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']

        if(ds.iloc[0].loc["success"]):
            return { 'success': True, 'message': ds.iloc[0].loc["message"] }

        return { 'success': False, 'message': ds.iloc[0].loc["message"] }
        

    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
