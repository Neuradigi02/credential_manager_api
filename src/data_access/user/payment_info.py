
    
from src.core.db import execute_query_async


def update_user_bank_details(user_id: str, bank_name: str, branch_name: str, ifscode: str, bank_account_no: str, account_holder_name: str, is_by_admin: bool, by_admin_user_id: str):
    res = execute_query_async("call usp_update_user_bank_details(_user_id => %s, _bank_name => %s, _branch_name => %s, _ifscode => %s, _bank_account_no => %s, _account_holder_name => %s, _is_by_admin => %s, _by_admin_user_id => %s)", 
    (user_id, bank_name, branch_name, ifscode, bank_account_no, account_holder_name, is_by_admin, by_admin_user_id))
    return res

    
def update_user_upi_details(user_id: str, upi_id: str, is_by_admin: bool, by_admin_user_id: str):
    res = execute_query_async("call usp_update_user_upi_details(_user_id => %s, _upi_id => %s, _is_by_admin => %s, _by_admin_user_id => %s)", 
    (user_id, upi_id, is_by_admin, by_admin_user_id))
    return res

    
def get_user_crypto_withdrawal_address(user_id: str, crypto_id: int=0):
    res = execute_query_async("call usp_get_user_crypto_withdrawal_address(_user_id => %s, _crypto_id => %s)", (user_id, crypto_id))
    return res


def add_user_crypto_withdrawal_address(user_id: str, crypto_id: str, address: str, is_by_admin: bool, by_admin_user_id: str):
    res = execute_query_async("call usp_insert_user_crypto_withdrawal_address(_user_id => %s, _crypto_id => %s, _address => %s, _is_by_admin => %s, _by_admin_user_id => %s)", 
    (user_id, crypto_id, address, is_by_admin, by_admin_user_id))
    return res

    
    