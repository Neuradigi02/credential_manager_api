
from typing import Union
from pydantic import BaseModel


class TokenData(BaseModel):
    user_id: Union[str, None] = None
    role: str = ''
    access_rights: str = ''
    token_id: int = 0
    token_type: str = 'HTTP'  # HTTP|WEBSOCKET


