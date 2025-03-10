
from typing import List
from pydantic import BaseModel


class MemberSearchRequest(BaseModel):
    user_id: str
    name: str
    email_id: str
    mobile_no: str
    active_status: str
    blocked_status: str
    joining_date_from: str=''
    joining_date_to: str=''
    page_index: int
    page_size: int
    
class MemberCountRequest(BaseModel):
    user_id: str
    left_active_directs_count: List[int]
    right_active_directs_count: List[int]
    total_active_directs_count: List[int]
    left_active_team_count: List[int]
    right_active_team_count: List[int]
    total_active_team_count: List[int]
    left_business: List[float]
    right_business: List[float]
    total_business: List[float]
    left_business_points: List[float]
    right_business_points: List[float]
    total_business_points: List[float]
    page_index: int
    page_size: int