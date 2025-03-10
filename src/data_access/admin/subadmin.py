
from src.core.db import execute_query_async


def get_sub_admin(by_admin_user_id):
    res = execute_query_async("call usp_get_sub_admins(_by_admin_user_id => %s)", (by_admin_user_id, ))
    return res

def add_new_admin(admin_user_id, password, mobile_no, email_id, by_admin_user_id):
    res = execute_query_async("call usp_add_new_admin(_admin_user_id => %s, _password => %s, _mobile_no => %s, _email_id => %s, _by_admin_user_id => %s)", (admin_user_id, password, mobile_no, email_id, by_admin_user_id))
    return res
    
def update_admin_access_rights(admin_user_id, access_rights, by_admin_user_id):
    res = execute_query_async("call usp_update_admin_access_rights(_admin_user_id => %s, _access_rights => %s, _by_admin_user_id => %s)", (admin_user_id, access_rights, by_admin_user_id))
    return res
    
def delete_admin(admin_user_id, by_admin_user_id):
    res = execute_query_async("call usp_delete_admin(_admin_user_id => %s, _by_admin_user_id => %s)", (admin_user_id, by_admin_user_id))
    return res