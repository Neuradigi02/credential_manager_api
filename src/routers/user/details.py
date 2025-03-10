
from typing import Annotated
from fastapi import APIRouter, Depends

from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants import VALIDATORS
from src.constants.messages import INVALID_USER_ID, OK, DATABASE_CONNECTION_ERROR
from src.data_access.user import details as data_access
from src.utilities.utils import data_frame_to_dict

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/details', dependencies=[Depends(RightsChecker([10, 11, 59]))])
async def details(user_id: Annotated[str, VALIDATORS.USER_ID], token_payload: any = Depends(get_current_user)):
    dataset = await data_access.get_user_details(user_id=user_id)
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["valid"]:
            if token_payload["role"] == 'User' and str(token_payload['user_id']).lower() != user_id.lower():
                ds = ds[['valid', 'user_id', 'name']]  # Only show necessary info to other users
            return {'success': True, 'message': OK, 'data': data_frame_to_dict(ds)}

    return {'success': False, 'message': INVALID_USER_ID }



@router.get('/dashboard_details', dependencies=[Depends(RightsChecker([12]))])
async def dashboard_details(token_payload: any = Depends(get_current_user)):
    user_id = token_payload["user_id"]

    dataset = await data_access.get_user_dashboard_details(user_id=user_id)
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["valid"]:
            return {'success': True,
                    'message': OK,
                    'data': data_frame_to_dict(ds),
                    'income': data_frame_to_dict(dataset['rs1']),
                    'wallet_balances': data_frame_to_dict(dataset['rs2']),
                    'news': data_frame_to_dict(dataset['rs_news'])}
        
        return {'success': False, 'message': INVALID_USER_ID }


@router.get('/dashboard_chart_details', dependencies=[Depends(RightsChecker([12]))])
async def dashboard_chart_details(duration: Annotated[str, VALIDATORS.CHART_DURATION], token_payload: any = Depends(get_current_user)):
    user_id = token_payload["user_id"]

    dataset = await data_access.get_user_dashboard_chart_details(user_id=user_id, duration=duration)
    if len(dataset):
        return {'success': True, 'message': OK, 'data': data_frame_to_dict(dataset['rs'])}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
