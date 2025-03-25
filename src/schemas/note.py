from typing import List
from pydantic import BaseModel



class ADD(BaseModel):
    title:str=''
    body:str=''


class update(BaseModel):
    note_id:int
    title:str
    body:str
    
  
class delete(BaseModel):
    note_id:int