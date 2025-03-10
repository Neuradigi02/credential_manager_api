
from typing import List
from src.schemas.MemberSearch import MemberCountRequest, MemberSearchRequest
from src.core.db import execute_query_async
from src.utilities.utils import process_js_datetime


def member_search(req: MemberSearchRequest):
    res = execute_query_async("""call usp_search_user(_user_id => %s, _name => %s, _email => %s, _mobile => %s, _joining_date => %s::timestamptz[], _active_status => %s, _blocked_status => %s,
    _page_index => %s, _page_size => %s)""", 
    (req.user_id, req.name, req.email_id, req.mobile_no, [process_js_datetime(req.joining_date_from), process_js_datetime(req.joining_date_to)], req.active_status, req.blocked_status, req.page_index, req.page_size))
    return res


def member_count(req: MemberCountRequest):
    res = execute_query_async("""call usp_get_member_count(_user_id => %s, _left_active_directs_count => %s::int[], _right_active_directs_count => %s::int[], _total_active_directs_count => %s::int[],
    _left_active_team_count => %s::int[], _right_active_team_count => %s::int[], _total_active_team_count => %s::int[], _left_business => %s::numeric[], _right_business=> %s::numeric[], _total_business => %s::numeric[], 
    _left_business_points => %s::numeric[], _right_business_points=> %s::numeric[], _total_business_points => %s::numeric[], _page_index => %s, _page_size => %s)""", 
    (req.user_id, req.left_active_directs_count, req.right_active_directs_count, req.total_active_directs_count, req.left_active_team_count, req.right_active_team_count,
    req.total_active_team_count, req.left_business, req.right_business, req.total_business, req.left_business_points, req.right_business_points, req.total_business_points, req.page_index, req.page_size))
    return res
    
    
def toggle_member_block_unblock(user_id: str, admin_user_id:str):
    res = execute_query_async("call usp_toggle_member_block_unblock(_user_id => %s, _admin_user_id => %s)", (user_id, admin_user_id))
    return res
    