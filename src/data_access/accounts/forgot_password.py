
from src.core.db import execute_query_async


def requestForResetPassword(user_id:str):
    return execute_query_async("call usp_request_for_reset_password(_user_id => %s)", (user_id, ))
    
def checkRequestForResetPasswordValidity(request_id:int):
    return execute_query_async("call usp_check_reset_password_request_validity(_request_id => %s)", (request_id, ))
    
def resetPassword(request_id:int, new_password:str):
    return execute_query_async("call usp_reset_password(_request_id => %s, _new_password => %s)", (request_id, new_password))
    