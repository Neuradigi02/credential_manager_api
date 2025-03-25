
from src.schemas.Accounts import Register
from src.core.db import execute_query_async


def is_sponsor_valid(sponsor_id:str):
    return execute_query_async("call usp_is_sponsor_valid(_sponsor_id => %s)", (sponsor_id, ))


def does_user_id_exist(user_id:str):
    return execute_query_async("call usp_does_user_id_exists(_user_id => %s)", (user_id, ))


def update_joining_mail_and_sms_status(user_id, is_email_sent, is_sms_sent):
    return execute_query_async("call usp_joining_mail_and_sms_status(_user_id => %s, _is_email_sent => %s, _is_sms_sent => %s)",
                         (user_id, is_email_sent, is_sms_sent))


def register(data: Register, is_email_verified: bool, is_mobile_verified: bool):
    return execute_query_async("""
    call usp_register(_sponsor_user_id => %s, _password => %s, _user_id => %s, _name => %s, _dob => %s, _marital_status => %s, _gender => %s, 
        _address => %s, _district => %s, _state => %s, _country => %s, _pincode => %s, _mobile => %s, _email => %s,
        _is_email_verified => %s, _is_mobile_verified => %s)""",
    (
        data.referralId if hasattr(data, 'referralId') else '',
        data.password if hasattr(data, 'password') else '',
        data.userId if hasattr(data, 'userId') else '',
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
        is_email_verified,
        is_mobile_verified
    ))
