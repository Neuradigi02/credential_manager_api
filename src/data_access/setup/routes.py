from src.schemas.Setup import AddRoute
from src.core.db import execute_query_async


def add_edit_route(req: AddRoute):
    res = execute_query_async("call usp_add_route(_id => %s, _parent_id => %s, _user_type => %s, _name => %s, "
                        "_path => %s, _description => %s, _mat_icon => %s, _css_classes => %s, _is_nav_menu_item => %s, "
                        "_is_active => %s, _order_no => %s, _nav_parent_id => %s, _is_compulsory => %s)",
                        (
                            req.id, req.parent_id, req.user_type, req.name, req.path, req.description, req.mat_icon,
                            req.css_classes, req.is_nav_menu_item, req.is_active, req.order_no,
                            req.nav_parent_id, req.is_compulsory
                         ))
    return res


def delete_route(id: int):
    res = execute_query_async("call usp_delete_route(_id => %s)", (id, ))
    return res


def update_active_routes(user_type: str, route_ids: str):
    res = execute_query_async("call usp_update_active_routes(_user_type => %s, _route_ids => %s)", (user_type, route_ids))
    return res
