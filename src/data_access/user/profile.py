
from src.core.db import execute_query_async
from src.utilities.utils import process_js_datetime


def update_user_personal_details(user_id:str, name:str, dob:str, gender:str, marital_status:str, is_by_admin:bool, by_admin_user_id: str):
    res = execute_query_async("call usp_update_user_personal_details(_user_id => %s, _name => %s, _dob => %s, _gender => %s, _marital_status => %s, _is_by_admin => %s, _by_admin_user_id => %s)", 
                              (user_id, name, process_js_datetime(dob), gender, marital_status, is_by_admin, by_admin_user_id))
    return res


def update_user_contact_details(user_id:str, email_id:str, mobile_no:str, address:str, district:str, pin_code:str, country:int, state:int, is_by_admin:bool, by_admin_user_id: str, two_factor_auth_request_id: int=0):
    res = execute_query_async("call usp_update_user_contact_details(_user_id => %s, _email_id => %s, _mobile_no => %s, _address => %s, _district => %s, _pin_code => %s, _country => %s, _state => %s, _is_by_admin => %s, _by_admin_user_id => %s, _two_factor_auth_request_id => %s)", 
    (user_id, email_id, mobile_no, address, district, pin_code, country, state, is_by_admin, by_admin_user_id, two_factor_auth_request_id))
    return res

    
def update_user_nominee_details(user_id:str, nominee_title:str, nominee_name:str, nominee_relationship:str, is_by_admin:bool, by_admin_user_id: str):
    res = execute_query_async("call usp_update_user_nominee_details(_user_id => %s, _nominee_title => %s, _nominee_name => %s, _nominee_relationship => %s, _is_by_admin => %s, _by_admin_user_id => %s)", 
    (user_id, nominee_title, nominee_name, nominee_relationship, is_by_admin, by_admin_user_id))
    return res

    