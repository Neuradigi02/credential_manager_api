
from typing import Annotated
from fastapi import APIRouter, Depends

from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants import VALIDATORS
from src.constants.messages import INVALID_USER_ID, OK, DATABASE_CONNECTION_ERROR
from src.data_access.admin import details as data_access
from src.utilities.utils import data_frame_to_dict

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/details', dependencies=[Depends(RightsChecker([11]))])
async def details(admin_user_id: Annotated[str, VALIDATORS.USER_ID], token_payload: any = Depends(get_current_user)):
    user_id_token = token_payload["user_id"]

    if admin_user_id == user_id_token:
        dataset = await data_access.get_admin_details(admin_user_id=admin_user_id)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["valid"]:
                return {'success': True, 'message': OK, 'data': data_frame_to_dict(ds)}
            
        return {'success': False, 'message': INVALID_USER_ID }
    return {'success': False, 'message': INVALID_USER_ID }


@router.get('/dashboard_details', dependencies=[Depends(RightsChecker([15]))])
async def dashboard_details(token_payload: any = Depends(get_current_user)):
    user_id = token_payload["user_id"]

    dataset = await data_access.get_admin_dashboard_details(admin_user_id=user_id)
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["valid"]:
            return {
                'success': True,
                'message': OK,
                'data': data_frame_to_dict(ds),
                'income_distribution': data_frame_to_dict(dataset['rs_income_distribution']),
                'packages_sales': data_frame_to_dict(dataset['rs_packages_sales'])
            }
        
        return {'success': False, 'message': INVALID_USER_ID }


@router.get('/dashboard_chart_details', dependencies=[Depends(RightsChecker([15]))])
async def dashboard_chart_details(duration: Annotated[str, VALIDATORS.CHART_DURATION], token_payload: any = Depends(get_current_user)):
    dataset = await data_access.get_admin_dashboard_chart_details(duration=duration)

    if len(dataset):
        return {'success': True, 'message': OK, 'data': data_frame_to_dict(dataset['rs'])}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


@router.get('/get_top_earners', dependencies=[Depends(RightsChecker([15]))])
async def get_top_earners(page_index: int = 0, page_size: int = 10, token_payload: any = Depends(get_current_user)):
    dataset = await data_access.get_top_earners(page_index=page_index, page_size=page_size)
    if len(dataset) > 0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_dict(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

