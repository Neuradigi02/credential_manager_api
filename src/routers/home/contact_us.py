
from fastapi import APIRouter

from src.constants.messages import DATABASE_CONNECTION_ERROR
from src.data_access.home import contact_us as data_access
from src.schemas.Home import ContactUs

router = APIRouter(
    prefix="/contact_us"
    )


@router.post('/save_message')
async def save_message(req: ContactUs):
    dataset =await data_access.save_message(name=req.name, email=req.email, type=req.type, subject=req.subject, message=req.message)

    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return {'success': True, 'message': ds.iloc[0].loc["message"] }
        
        return {'success': False, 'message': ds.iloc[0].loc["message"] }
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR }

