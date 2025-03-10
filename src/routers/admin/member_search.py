from fastapi import APIRouter, Depends

from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.admin import member_search as data_access
from src.schemas.MemberSearch import MemberCountRequest, MemberSearchRequest
from src.utilities.utils import data_frame_to_dict

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/member_search', dependencies=[Depends(RightsChecker([26])), Depends(get_current_user)])
async def member_search(req: MemberSearchRequest):
    dataset = await data_access.member_search(req)
    if len(dataset)>0:
        ds = dataset['rs']
        return { 'success': True, 'message': OK, 'data': data_frame_to_dict(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}
            
    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.post('/member_count', dependencies=[Depends(RightsChecker([26])), Depends(get_current_user)])
async def member_search(req: MemberCountRequest):
    dataset = await data_access.member_count(req)
    if len(dataset)>0:
        ds = dataset['rs']
        return { 'success': True, 'message': OK, 'data': data_frame_to_dict(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}
            
    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }


# @router.post('/member_search_export_to_csv', dependencies=[Depends(RightsChecker([26])), Depends(get_current_user)])
# async def member_search(req: MemberSearchRequest):
    # dataset = await data_access.member_search(req)
    # if len(dataset)>0:
    #     ds = dataset['rs']
        
    #     stream = io.StringIO()
    #     ds.to_csv(stream, sep=";",index=False)
    #     return { 'success': True, 'message': OK, 'data': stream.getvalue() }

    # return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.get('/toggle_member_block_unblock', dependencies=[Depends(RightsChecker([26]))])
async def toggle_member_block_unblock(user_id: str, token_payload: any = Depends(get_current_user)):
    by_admin_user_id = token_payload["user_id"]
    dataset = await data_access.toggle_member_block_unblock(user_id=user_id, admin_user_id=by_admin_user_id)

    if len(dataset)>0:
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return { 'success': True, 'message': ds.iloc[0].loc["message"] }
            
    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
