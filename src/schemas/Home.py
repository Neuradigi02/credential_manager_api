
from pydantic import BaseModel


class ContactUs(BaseModel):
    name: str
    email: str
    type: str
    subject: str
    message: str