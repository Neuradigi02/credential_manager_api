from typing import List
from pydantic import BaseModel

class add_label(BaseModel):
   name:str

class update_label(BaseModel):
    label_id:int
    name:str

class delete_label(BaseModel):
    label_id:int