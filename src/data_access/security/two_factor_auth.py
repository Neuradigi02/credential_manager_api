
from src.core.db import execute_query_async

def toggle_two_factor_auth(user_id: str, user_type: str, two_factor_auth_request_id: int):
    res = execute_query_async("call usp_toggle_two_factor_auth(_user_id => %s, _user_type => %s, _two_factor_auth_request_id => %s)", (user_id, user_type, two_factor_auth_request_id))
    return res

def toggle_google_authenticator(user_id: str, user_type: str):
    res = execute_query_async("call usp_toggle_google_auth(_user_id => %s, _user_type => %s)", (user_id, user_type))
    return res

def setup_google_authenticator(user_id: str, user_type: str, secret_key: str):
    res = execute_query_async("call usp_setup_google_auth(_user_id => %s, _user_type => %s, _secret_key => %s)", (user_id, user_type, secret_key))
    return res

def request_two_factor_auth(user_id: str, user_type: str, purpose: str):
    res = execute_query_async("call usp_request_two_factor_auth(_user_id => %s, _user_type => %s, _purpose => %s)", (user_id, user_type, purpose))
    return res

def get_auth_modes(user_id: str, request_id: int):
    res = execute_query_async("call usp_get_two_factor_auth_modes(_user_id => %s, _request_id => %s)", (user_id, request_id))
    return res
    
def get_auth_modes_for_setup(user_id: str, user_type: str):
    res = execute_query_async("call usp_get_2fa_modes_for_setup(_user_id => %s, _user_type => %s)", (user_id, user_type))
    return res
    
def submit_two_factor_auth_code(request_id:int, mode: str, code: str):
    return execute_query_async("call usp_submit_two_factor_auth_code(_request_id => %s, _mode => %s, _code => %s)", (request_id, mode, code))
