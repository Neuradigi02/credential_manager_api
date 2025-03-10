
from src.core.db import execute_query_async


def getOTPForContactVerification(user_id: str, contact_type: str, email_id_or_mobile_no: str):
    return execute_query_async("call usp_request_otp_for_contact_verification(_user_id => %s, _contact_type => %s, _email_id_or_mobile_no => %s)", (user_id, contact_type, email_id_or_mobile_no))


def submitOTPForContactVerification(user_id: str, contact_type: str, email_id_or_mobile_no: str, otp: str):
    return execute_query_async("call usp_submit_otp_for_contact_verification(_user_id => %s, _contact_type => %s, _email_id_or_mobile_no => %s, _otp => %s)", (user_id, contact_type, email_id_or_mobile_no, otp))
