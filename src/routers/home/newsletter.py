
from fastapi import APIRouter

from src.constants.messages import DATABASE_CONNECTION_ERROR
from src.data_access.home import newsletter as data_access

router = APIRouter(
    prefix="/newsletter"
    )

@router.get('/subscribe')
async def subscribe(email: str):
    dataset = await data_access.newsletter_subscription(email=email, subscription_status=True)

    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return {'success': True, 'message': ds.iloc[0].loc["message"] }
        
        return {'success': False, 'message': ds.iloc[0].loc["message"] }
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR }


@router.get('/unsubscribe')
async def unsubscribe(email: str):
    dataset = await data_access.newsletter_subscription(email=email, subscription_status=False)

    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return {'success': True, 'message': ds.iloc[0].loc["message"] }
        
        return {'success': False, 'message': ds.iloc[0].loc["message"] }
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
