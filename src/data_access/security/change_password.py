
from src.core.db import execute_query_async


def changePassword(user_id:str, user_type:str, old_password:str, new_password:str, is_by_admin: bool, by_admin_user_id: str, two_factor_auth_request_id: int=0):
    res = execute_query_async("call usp_change_password(_user_id => %s, _user_type => %s, _old_password => %s, _new_password => %s, _is_by_admin => %s, _by_admin_user_id => %s, _two_factor_auth_request_id => %s)",
                        (user_id, user_type, old_password, new_password, is_by_admin, by_admin_user_id, two_factor_auth_request_id))
    return res
    