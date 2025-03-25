
from src.core.db import execute_query_async


def get_all_routes():
    return execute_query_async("call usp_get_all_routes()")


def get_countries():
    return execute_query_async("call usp_get_countries()")


def get_states_by_country_id(country_id: int):
    res = execute_query_async("call usp_get_states_by_country_id(_country_id => %s)", (country_id,))
    return res


def get_column_details(report_name: str):
    res = execute_query_async("call usp_get_columns(_report_name => %s)", (report_name, ))
    return res


def filter_user_ids(filter_value: str, user_type: str):
    res = execute_query_async("call usp_filter_user_ids(_user_id => %s, _user_type => %s)", (filter_value, user_type))
    return res

