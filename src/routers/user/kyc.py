import orjson
from fastapi import APIRouter, Depends
from src.core.security.Jwt import get_current_user
from src.core.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.user import kyc as data_access
from src.schemas.KYC import KYCRequest, GetKYCRequest, KycRequestApproveRejectDataItem
from src.utilities.utils import save_base64_file, data_frame_to_dict

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/request_for_kyc', dependencies=[Depends(RightsChecker([173]))])
async def request_for_kyc(req: KYCRequest, token_payload: any = Depends(get_current_user)):
    user_id = token_payload["user_id"]

    req.aadhaar_front_image, path = save_base64_file(req.aadhaar_front_image, upload_file_name='KYC_Aadhaar_Front')

    req.aadhaar_back_image, path = save_base64_file(req.aadhaar_back_image, upload_file_name='KYC_Aadhaar_Back')

    req.pan_image, path = save_base64_file(req.pan_image, upload_file_name='KYC_PAN')

    dataset = await data_access.request_for_kyc(user_id=user_id, req=req)
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']

        if ds.iloc[0].loc["success"]:
            return {'success': True, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': ds.iloc[0].loc["message"]}
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


@router.post('/get_kyc_requests', dependencies=[Depends(RightsChecker([173, 174]))])
async def get_kyc_requests(req: GetKYCRequest, token_payload: any = Depends(get_current_user)):
    match_exact_user_id = False
    if token_payload["role"] == 'User':
        req.user_id = token_payload["user_id"]
        match_exact_user_id = True

    dataset = await data_access.get_kyc_requests(req=req, match_exact_user_id=match_exact_user_id)

    if len(dataset) > 0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_dict(ds),
                'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}



@router.put('/update_kyc_requests_status', dependencies=[Depends(RightsChecker([174]))])
async def update_kyc_requests_status(dataItems: list[KycRequestApproveRejectDataItem], token_payload: any = Depends(get_current_user)):
    user_id = token_payload["user_id"]

    data_dicts = orjson.dumps([item.dict() for item in dataItems]).decode("utf-8")
    
    dataset = await data_access.update_kyc_requests_status(by_user_id=user_id, data_dicts = data_dicts)
    if len(dataset) > 0:
        ds = dataset['rs']
        if (ds.iloc[0].loc["success"]):
            return {
                'success': True,
                'message': ds.iloc[0].loc["message"],
                'approved_count': int(ds.iloc[0].loc["approved_count"]),
                'rejected_count': int(ds.iloc[0].loc["rejected_count"])
            }

        return {'success': False, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


