
from fastapi import APIRouter, Request
from src.constants.messages import DATABASE_CONNECTION_ERROR
from src.data_access.home import visitors as data_access
from src.utilities.app_utils import get_ip_info
from src.core.load_config import config
from src.utilities.company_util import company_details
from src.utilities.utils import get_real_client_ip


router = APIRouter()


@router.get('/')
async def visited(request: Request):
    url = dict(request.scope["headers"]).get(b"referer", b"").decode() # request.base_url.__str__()
    
    client_ip_address = get_real_client_ip(request)

    ip_details = await get_ip_info(client_ip_address)

    dataset = await data_access.save_visitor(url=url, ip_address=client_ip_address, ip_details=ip_details)

    if len(dataset) > 0:

        login_info_df = dataset['rs']

        if len(login_info_df) > 0:
            return {'success': True, 'message': 'Welcome to '+company_details['name']+' API'}
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
