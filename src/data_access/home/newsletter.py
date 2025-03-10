
from src.core.db import execute_query_async


def newsletter_subscription(email: str, subscription_status: bool):
    res = execute_query_async("call usp_subscribe_newsletter(_email => %s, _subscription_status => %s)", (email, subscription_status))
    return res