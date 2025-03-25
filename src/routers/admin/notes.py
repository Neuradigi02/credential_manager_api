from fastapi import APIRouter, Depends

from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.schemas.note import ADD,update,delete
from src.data_access.admin import add_notes as data_access
from src.utilities.utils import data_frame_to_dict


router = APIRouter( dependencies=[Depends(get_current_user)]
)

@router.post('/add_note', dependencies=[Depends(RightsChecker([10]))])
async def add_note(req: ADD,token_payload:any=Depends(get_current_user)):
    by_user_id=token_payload['user_id']
    dataset = await data_access.add_notes(req=req,user_id=by_user_id)


    if len(dataset)>0:
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return { 'success': True, 'message': ds.iloc[0].loc["message"] }
        return{'success':False,'message':ds.iloc[0].loc["message"]}    
    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.put('/update_note', dependencies=[Depends(RightsChecker([10]))])
async def update_note(req:update,token_payload:any=Depends(get_current_user)):
    by_user_id=token_payload['user_id']
    dataset = await data_access.update_note(req=req,user_id=by_user_id)

    if len(dataset)>0:
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return { 'success': True, 'message': ds.iloc[0].loc["message"]}
        return{'success':False,'message':ds.iloc[0].loc["message"]}    
    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.delete('/delete', dependencies=[Depends(RightsChecker([10]))])
async def delete_note(req:delete,token_payload:any=Depends(get_current_user)):
    by_user_id=token_payload['user_id']
    dataset = await data_access.delete_note(req=req,user_id=by_user_id)


    if len(dataset)>0:
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return { 'success': True, 'message': ds.iloc[0].loc["message"] }
        return{'success':False,'message':ds.iloc[0].loc["message"]}    
    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
