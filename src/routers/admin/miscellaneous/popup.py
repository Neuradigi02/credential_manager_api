from fastapi import APIRouter, Depends

from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_FILE_TYPE, OK
from src.data_access.admin.miscellaneous import popup as data_access
from src.schemas.Admin_Miscellaneous import AddPopup
from src.utilities.utils import save_base64_file, data_frame_to_dict

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/add_popup', dependencies=[Depends(RightsChecker([235]))])
async def add_popup(req: AddPopup, token_payload: any = Depends(get_current_user)):
    by_admin_id = token_payload["user_id"]

    if req.image_base_64 == '':
        return {'success': False, 'message': INVALID_FILE_TYPE}

    file_name, path = save_base64_file(req.image_base_64, upload_file_name='Popup')

    dataset = await data_access.add_popup(user_type=req.user_type, file_name=file_name, admin_user_id=by_admin_id)
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["success"]:
            return {'success': True, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}



@router.get('/get_popups', dependencies=[Depends(RightsChecker([235]))])
async def get_popups(page_index: int, page_size: int, token_payload: any = Depends(get_current_user)):
    dataset = await data_access.get_popups(page_index=page_index, page_size=page_size)
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_dict(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}



@router.get('/toggle_popup', dependencies=[Depends(RightsChecker([235]))])
async def toggle_popup(popup_id: int, token_payload: any = Depends(get_current_user)):
    dataset = await data_access.toggle_popup(popup_id=popup_id)
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        return {'success': True, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


@router.delete('/delete_popup', dependencies=[Depends(RightsChecker([235]))])
async def delete_popup(popup_id: int, token_payload: any = Depends(get_current_user)):
    dataset = await data_access.delete_popup(popup_id=popup_id)
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        return {'success': True, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


