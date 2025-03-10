from typing import List
from fastapi import Depends, HTTPException
from src.core.security.Jwt import get_current_user, verify_ws_token
from src.utilities.utils import intersection


class RightsChecker:
    def __init__(self, access_rights: List):
        self.access_rights = access_rights

    def __call__(self, user = Depends(get_current_user)):
        user_rights = [int(right) for right in user['access_rights'].split(',')]
        if len(intersection(user_rights, self.access_rights))==0:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        
        
async def rights_checker_ws(token, allowed_rights: List):
    payload =await verify_ws_token(token)
    user_rights = [int(right) for right in payload['access_rights'].split(',')]
    if len(intersection(user_rights, allowed_rights)) == 0:
        raise HTTPException(status_code=403, detail="Operation not permitted")
