from fastapi import APIRouter,Depends
from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.schemas.label_note_schema import add_label,update_label,delete_label
from src.data_access.admin import label_note as data_access
from src.utilities.utils import data_frame_to_dict


router=APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post('/label_add_note',dependencies=[Depends(RightsChecker([10]))])
async def label_add_note(req:add_label,token_payload:any=Depends(get_current_user)):
    by_user_id=token_payload['user_id']
    dataset = await data_access.label_add_notes(req=req,user_id=by_user_id)

    # if len(dataset)>0:
    #     ds=dataset['rs']
    #     if (ds.iloc[0].loc['success']):
    #         return {'success': True,'message':ds.iloc[0].loc["message"]}
    #     return{'success': False,'message':ds.iloc[0].loc['message']}
    # return{'success':False,'message':DATABASE_CONNECTION_ERROR}
    if len(dataset)>0:
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return { 'success': True, 'message': ds.iloc[0].loc["message"] }
        return{'success':False,'message':ds.iloc[0].loc["message"]}    
    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.put('/label_update_note',dependencies=[Depends(RightsChecker([10]))])
async def label_update_note(req:update_label,token_payload:any=Depends(get_current_user)):
    by_user_id=token_payload['user_id']
    dataset = await data_access.label_update_note(req=req,user_id=by_user_id)


    if len(dataset)>0:
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return { 'success': True, 'message': ds.iloc[0].loc["message"] }
        return{'success':False,'message':ds.iloc[0].loc["message"]}    
    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }



@router.delete('/label_delete_note',dependencies=[Depends(RightsChecker([10]))])
async def label_delete_note(req:delete_label,token_payload:any=Depends(get_current_user)):
    by_user_id=token_payload['user_id']
    dataset = await data_access.label_delete_note(req=req,user_id=by_user_id)

    if len(dataset)>0:
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return { 'success': True, 'message': ds.iloc[0].loc["message"] }
        return{'success':False,'message':ds.iloc[0].loc["message"]}    
    return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }