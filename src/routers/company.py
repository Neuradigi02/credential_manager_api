from fastapi import APIRouter
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.utilities.company_util import company_details


router = APIRouter(prefix="/company", tags=["Company"])


@router.get('/details')
def get_details():
    dataset = company_details.to_dict()

    if dataset:
        return {
            'success': True, 
            'message': OK, 
            'data': dataset
            }
        
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
