from typing import List
from src.core.db import execute_query_async
from src.schemas.note import ADD,update,delete,
from src.utilities.utils import process_js_datetime


def add_notes(req:ADD,user_id):
    res = execute_query_async("call usp_add_note(_user_id => %s, _title => %s,_body => %s)", (user_id, req.title,req.body ))
    return res
    

def update_note(req:update,user_id):
    res = execute_query_async("call usp_update_note(_user_id => %s,_note_id=> %s, _title => %s,_body => %s)", 
                              (user_id,req.note_id , req.title,req.body ))
    return res

def delete_note(req:delete,user_id):
    res = execute_query_async("call usp_delete_note(_user_id => %s,_note_id=> %s)", 
                              (user_id,req.note_id ))
    return res