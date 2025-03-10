
from src.core.db import execute_query_async


def login(user_id: str, password: str, url: str, host: str, ip_details, by_admin_user_id: str):
    res = execute_query_async("call usp_login(_user_id => %s, _password => %s, _url => %s, _ip_address =>%s, _ip_details => %s::json, _by_admin_user_id => %s)",
                        (user_id, password, url, host, ip_details, by_admin_user_id))
    return res


def is_valid_login_id(login_id: str, user_id: str):
    return execute_query_async("call usp_is_valid_login_id(_login_id => %s, _user_id => %s)", (login_id, user_id))


def can_get_login_token(login_id: int, user_id: str):
    return execute_query_async("call usp_can_get_login_token(_login_id => %s, _user_id => %s)", (login_id, user_id))


def is_valid_token(token_id: int):
    return execute_query_async("call usp_is_valid_token(_token_id => %s)", (token_id, ))


def get_user_id_from_member_id(member_id: int):
    return execute_query_async("call usp_get_user_id_from_member_id(_member_id => %s)", (member_id, ))
