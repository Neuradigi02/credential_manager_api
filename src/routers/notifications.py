from fastapi import APIRouter, Depends

from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access import notifications as data_access
from src.utilities.utils import data_frame_to_dict

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get('/get_notifications', dependencies=[Depends(RightsChecker([10, 11, 59]))])
async def get_notifications(page_index: int = 0, page_size: int = 10, token_payload: any = Depends(get_current_user)):
    user_id = token_payload["user_id"]
    dataset = await data_access.get_notifications(user_id=user_id, page_index=page_index, page_size=page_size)
    
    if len(dataset) > 0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_dict(ds),
                'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]),
                'unread_count': int(dataset['rs1'].iloc[0].loc["unread_count"])}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


@router.put('/mark_as_read', dependencies=[Depends(RightsChecker([10, 11, 59]))])
async def mark_as_read(message_ids: str, token_payload: any = Depends(get_current_user)):
    # message_ids = [int(id) for id in message_ids.split(',')]

    dataset = await data_access.mark_as_read(message_ids=message_ids, user_id=token_payload["user_id"],
                                        user_type=token_payload["role"])
    
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["success"]:
            return {'success': True, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

