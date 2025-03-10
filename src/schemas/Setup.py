from pydantic import BaseModel


class AddRoute(BaseModel):
    id: int = None
    parent_id: int = 0
    user_type: str
    name: str
    path: str
    description: str = ''
    mat_icon: str = ''
    css_classes: str = ''
    is_nav_menu_item: bool = False
    is_active: bool = True
    order_no: int = 0
    nav_parent_id: int = 0
    is_compulsory: bool = False


class UpdateActiveRoutes(BaseModel):
    user_type: str
    route_ids: str