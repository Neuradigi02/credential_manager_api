
from src.core.db import execute_query_async


def save_visitor(url: str, ip_address: str, ip_details):
    res = execute_query_async("call usp_save_visitor(_url => %s, _ip_address => %s, _ip_details => %s::json)", (url, ip_address, ip_details))
    return res