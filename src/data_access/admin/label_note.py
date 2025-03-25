from typing import List
from src.core.db import execute_query_async
from src.schemas.label_note_schema import add_label,update_label,delete_label

def label_add_notes(req:add_label,user_id):
    res = execute_query_async("call usp_add_label(_user_id => %s, _name => %s)", (user_id, req.name ))
    return res


def label_update_note(req:update_label,user_id):
    res =execute_query_async("call usp_update_label(_user_id => %s,_label_id=>%s, _name => %s)",(user_id, req.label_id,req.name ))
    return res

def label_delete_note(req:delete_label,user_id):
    res =execute_query_async("call usp_delete_label(_user_id => %s,_label_id => %s)",(user_id,req.label_id ))
    return res