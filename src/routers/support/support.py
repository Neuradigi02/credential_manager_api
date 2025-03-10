
from fastapi import APIRouter, Depends

from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.data_access.support import support as data_access
from src.schemas.Support import Messages, ComposeMessageRequest
from src.utilities.utils import data_frame_to_dict, save_base64_file

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post('/compose', dependencies=[Depends(RightsChecker([121, 122, 123]))])
async def compose(req: ComposeMessageRequest, token_payload: any = Depends(get_current_user)):
    attachment_name = ''
    if req.attachment != '':
        attachment_name, path = save_base64_file(req.attachment, upload_file_name='Attachment')

    dataset = await data_access.compose(to_user_ids=req.to_user_ids, to_user_type=req.to_user_type, is_send_to_all=req.is_send_to_all,
                                    subject=req.subject, message=req.message, by_user_id=token_payload["user_id"],
                                    by_user_type=token_payload["role"], attachment_name=attachment_name)

    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["success"]:
            return {'success': True, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}



@router.post('/messages', dependencies=[Depends(RightsChecker([124, 125, 126, 127, 128, 129]))])
async def messages(req: Messages, token_payload: any = Depends(get_current_user)):
    dataset = await data_access.messages(req=req, user_id=token_payload["user_id"], user_type=token_payload["role"])

    if len(dataset) > 0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_dict(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]), 'unread_count': int(dataset['rs1'].iloc[0].loc["unread_count"])}
        
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}



@router.put('/mark_as_read', dependencies=[Depends(RightsChecker([124, 125, 126]))])
async def mark_as_read(message_id: int, token_payload: any = Depends(get_current_user)):
    dataset = await data_access.mark_as_read(message_id=message_id, user_id=token_payload["user_id"], user_type=token_payload["role"])

    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["success"]:
            
            return {'success': True, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}



@router.delete('/delete_messages', dependencies=[Depends(RightsChecker([124, 125, 126]))])
async def delete_messages(message_ids: str, token_payload: any = Depends(get_current_user)):
    message_ids = [int(i) for i in message_ids.split(',')]
    
    dataset = await data_access.delete_messages(message_ids=message_ids, user_id=token_payload["user_id"], user_type=token_payload["role"])

    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["success"]:
            
            return {'success': True, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

