
from src.core.db import execute_query_async


def update_admin_details(user_id:str, email_id:str, mobile_no:str, by_admin_user_id: str, two_factor_auth_request_id: str = ''):
    res = execute_query_async("call usp_update_admin_details(_admin_user_id => %s, _email_id => %s, _mobile_no => %s, _by_admin_user_id => %s, _two_factor_auth_request_id => %s)", 
    (user_id, email_id, mobile_no, by_admin_user_id, two_factor_auth_request_id))
    return res
