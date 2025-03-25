from typing import Annotated
from fastapi import APIRouter, Depends
import pyqrcode
from fastapi import APIRouter, Depends

from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants import VALIDATORS
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access import misc as data_access
from src.utilities.utils import data_frame_to_dict

router = APIRouter(
    prefix="/misc",
    tags=["Miscellaneous"]
)


@router.get('/get_countries')
async def get_countries():
    dataset = await data_access.get_countries()

    if len(dataset) > 0:
        df = dataset['rs']

        if len(df) > 0:
            df = data_frame_to_dict(df)
            return {'success': True, 'message': OK, 'data': df }
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    

@router.get('/get_states_by_country_id')
async def get_states_by_country_id(country_id: int):
    dataset = await data_access.get_states_by_country_id(country_id=country_id)
    if len(dataset) > 0:
        df = dataset['rs']

        if len(df) > 0:
            df = data_frame_to_dict(df)
            return {'success': True, 'message': OK, 'data': df }
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    

@router.get('/get_qr')
async def get_qr(value: str):
    qr = pyqrcode.create(value)
    return {'success': True, 'message': OK, 'qr': "data:image/png;base64,"+qr.png_as_base64_str(scale=5) }
    

@router.get('/get_column_details')
async def get_column_details(report_name: str):
    dataset = await data_access.get_column_details(report_name=report_name)
    if len(dataset) > 0:
        df = dataset['rs']

        if len(df) > 0:
            df = data_frame_to_dict(df)
            return {'success': True, 'message': OK, 'data': df}
            
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    

@router.get('/filter_user_ids', dependencies=[Depends(RightsChecker([104]))])
async def filter_user_ids(filter_value: str, user_type: Annotated[str, VALIDATORS.USER_TYPE], token_payload: any = Depends(get_current_user)):

    # start_time = time.time()
    if token_payload['role'] == 'User':
        user_type = 'User'

    dataset = await data_access.filter_user_ids(filter_value=filter_value, user_type=user_type)
    if len(dataset) > 0:
        df = dataset['rs']
        # end_time = time.time()
        return {'success': True, 'message': OK, 'data': data_frame_to_dict(df)}
            
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

