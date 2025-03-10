
from fastapi import APIRouter, Depends

from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.admin import subadmin as data_access
from src.schemas.Admin import AddNewAdminRequest, AdminAccessRightsUpdateRequest
from src.utilities.utils import data_frame_to_dict

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get('/get_sub_admins', dependencies=[Depends(RightsChecker([20]))])
async def get_sub_admins(token_payload:any = Depends(get_current_user)):
    by_admin_id = token_payload["user_id"]
    
    dataset = await data_access.get_sub_admin(by_admin_user_id=by_admin_id)
    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_dict(ds)}
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}



@router.post('/add_new_admin', dependencies=[Depends(RightsChecker([20,21]))])
async def add_new_admin(req: AddNewAdminRequest, token_payload:any = Depends(get_current_user)):
    by_admin_id = token_payload["user_id"]

    dataset = await data_access.add_new_admin(admin_user_id=req.admin_user_id, password=req.password, email_id=req.email_id, mobile_no=req.mobile_no, by_admin_user_id=by_admin_id)
    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return {'success': True, 'message': ds.iloc[0].loc["message"] }
        
        return {'success': False, 'message': ds.iloc[0].loc["message"] }
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


@router.put('/update_access_rights', dependencies=[Depends(RightsChecker([20,23]))])
async def update_access_rights(req: AdminAccessRightsUpdateRequest, token_payload:any = Depends(get_current_user)):
    by_admin_id = token_payload["user_id"]

    dataset = await data_access.update_admin_access_rights(admin_user_id=req.user_id, access_rights=req.access_rights, by_admin_user_id=by_admin_id)
    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return {'success': True, 'message': ds.iloc[0].loc["message"] }
        
        return {'success': False, 'message': ds.iloc[0].loc["message"] }
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


@router.delete('/delete_admin', dependencies=[Depends(RightsChecker([20]))])
async def delete_admin(admin_id: str, token_payload:any = Depends(get_current_user)):
    by_admin_id = token_payload["user_id"]

    dataset = await data_access.delete_admin(admin_user_id=admin_id, by_admin_user_id=by_admin_id)
    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return {'success': True, 'message': ds.iloc[0].loc["message"] }
        
        return {'success': False, 'message': ds.iloc[0].loc["message"] }
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
