
from src.schemas.Support import Messages
from src.core.db import execute_query_async


def compose(to_user_ids: list, to_user_type: str, is_send_to_all: bool, subject: str, message: str, by_user_id: str, by_user_type: str, attachment_name: str):
    res = execute_query_async("call usp_insert_support_meesage(_to_user_ids => %s, _to_user_type => %s, _subject => %s, _message => %s, _by_user_id => %s, _by_user_type => %s, _is_send_to_all => %s, _attachment_name => %s)",
                        (to_user_ids, to_user_type, subject, message, by_user_id, by_user_type, is_send_to_all, attachment_name))
    return res


def messages(req: Messages, user_id: str, user_type: str):
    res = execute_query_async("call usp_get_support_messages(_user_id => %s, _user_type => %s, _search_string => %s, _type => %s, _page_index => %s, _page_size => %s)",
                        (user_id, user_type, req.search_string, req.type, req.page_index, req.page_size))
    return res


def mark_as_read(message_id: int, user_id: str, user_type: str):
    res = execute_query_async("call usp_update_support_message_read_status(_user_id => %s, _user_type => %s, _message_id => %s)",
                        (user_id, user_type, message_id))
    return res


def delete_messages(message_ids: list[int], user_id: str, user_type: str):
    res = execute_query_async("call usp_delete_support_message(_user_id => %s, _user_type => %s, _message_ids => %s)",
                        (user_id, user_type, message_ids))
    return res
