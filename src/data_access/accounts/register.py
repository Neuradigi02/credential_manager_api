
from src.schemas.Accounts import Register
from src.core.db import execute_query_async


def is_sponsor_valid(sponsor_id:str):
    return execute_query_async("call usp_is_sponsor_valid(_sponsor_id => %s)", (sponsor_id, ))


def is_upline_valid(upline_user_id:str):
    return execute_query_async("call usp_is_upline_valid(_upline_user_id => %s)", (upline_user_id, ))


def does_user_id_exist(user_id:str):
    return execute_query_async("call usp_does_user_id_exists(_user_id => %s)", (user_id, ))


def update_joining_mail_and_sms_status(user_id, is_email_sent, is_sms_sent):
    return execute_query_async("call usp_joining_mail_and_sms_status(_user_id => %s, _is_email_sent => %s, _is_sms_sent => %s)",
                         (user_id, is_email_sent, is_sms_sent))


def register(data: Register, is_email_verified: bool, is_mobile_verified: bool):
    return execute_query_async("""
    call usp_register(_sponsor_user_id => %s, _password => %s, _user_id => %s, _pin_number => %s, _pin_password => %s, 
        _upline_user_id => %s,  _side => %s, _name => %s, _dob => %s, _marital_status => %s, _gender => %s, 
        _address => %s, _district => %s, _state => %s, _country => %s, _pincode => %s, _mobile => %s, _email => %s, 
        _nominee_title => %s, _nominee_name => %s, _nominee_relationship => %s, _ifscode => %s, _bank_name => %s, 
        _branch_name => %s, _bank_account_number => %s, _account_holder_name => %s, _pan_card_number => %s, 
        _is_email_verified => %s, _is_mobile_verified => %s)""",
    (
        data.referralId if hasattr(data, 'referralId') else '',
        data.password if hasattr(data, 'password') else '',
        data.userId if hasattr(data, 'userId') else '', 
        data.pinNumber if hasattr(data, 'pinNumber') else 0,
        data.pinPassword if hasattr(data, 'pinPassword') else 0,
        data.uplineId if hasattr(data, 'uplineId') else '', 
        data.side if hasattr(data, 'side') else '', 
        data.name if hasattr(data, 'name') else '', 
        data.dob if hasattr(data, 'dob') else None, 
        data.maritalStatus if hasattr(data, 'maritalStatus') else 'S', 
        data.gender if hasattr(data, 'gender') else 'M', 
        data.address if hasattr(data, 'address') else '', 
        data.district if hasattr(data, 'district') else '', 
        data.state if hasattr(data, 'state') else 0, 
        data.country if hasattr(data, 'country') else 0, 
        data.pincode if hasattr(data, 'pincode') else '', 
        data.mobile if hasattr(data, 'mobile') else '', 
        data.email if hasattr(data, 'email') else '', 
        data.nomineeTitle if hasattr(data, 'nomineeTitle') else 'Mr', 
        data.nomineeName if hasattr(data, 'nomineeName') else '', 
        data.nomineeRelationship if hasattr(data, 'nomineeRelationship') else '', 
        data.IFSCode if hasattr(data, 'IFSCode') else '', 
        data.bankName if hasattr(data, 'bankName') else '', 
        data.branchName if hasattr(data, 'branchName') else '', 
        data.bankAccountNumber if hasattr(data, 'bankAccountNumber') else '', 
        data.accountHolderName if hasattr(data, 'accountHolderName') else '', 
        data.panCardNumber if hasattr(data, 'panCardNumber') else '',
        is_email_verified,
        is_mobile_verified
    ))
