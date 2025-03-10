from typing import Annotated
from pydantic import BaseModel

from src.constants import VALIDATORS


class AddNews(BaseModel):
    news_id: int = 0
    user_type: Annotated[str, VALIDATORS.USER_TYPE_ALL] = 'All'  
    heading: str
    details: str
    priority: int = 1


class AddPopup(BaseModel):
    user_type: Annotated[str, VALIDATORS.USER_TYPE_ALL] = 'All'
    image_base_64: Annotated[str, VALIDATORS.REQUIRED]
