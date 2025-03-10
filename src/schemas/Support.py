
from typing import Annotated
from pydantic import BaseModel
from src.constants import VALIDATORS


class ComposeMessageRequest(BaseModel):
    to_user_ids: list
    to_user_type: str
    subject: str
    message: str
    is_send_to_all: bool = False
    attachment: str = ''


class Messages(BaseModel):
    search_string: str=''
    type: Annotated[str, VALIDATORS.SUPPORT_MESSAGES_TYPE] = 'Inbox'
    page_index: int=0
    page_size: int=100


