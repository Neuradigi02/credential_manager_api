from src.core.db import execute_query_async


def get_notifications(user_id: str, page_index: int = 0, page_size: int = 10):
    res = execute_query_async("call usp_get_notifications(_user_id => %s, _page_index => %s, _page_size => %s)",
                        (user_id, page_index, page_size))
    return res


def mark_as_read(message_ids: str, user_id: str, user_type: str):
    res = execute_query_async("call usp_update_notification_read_status(_user_id => %s, _user_type => %s, _message_ids => %s)",
                        (user_id, user_type, message_ids))
    return res
