from src.schemas.Admin_Miscellaneous import AddPopup
from src.core.db import execute_query_async


def add_popup(user_type: str, file_name: str, admin_user_id: str):
    res = execute_query_async("call usp_add_popup(_user_type => %s, _image_file_name => %s, _by_admin_user_id => %s)",
                        (user_type, file_name, admin_user_id))
    return res


def get_popups(page_index: int, page_size: int):
    res = execute_query_async("call usp_get_popups(_page_index => %s, _page_size => %s)", (page_index, page_size))
    return res


def toggle_popup(popup_id: int):
    res = execute_query_async("call usp_toggle_popup(_popup_id => %s)", (popup_id, ))
    return res


def delete_popup(popup_id: int):
    res = execute_query_async("call usp_delete_popup(_popup_id => %s)", (popup_id, ))
    return res
