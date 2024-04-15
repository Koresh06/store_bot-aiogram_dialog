from .admin.handler import admin_router
from .users.handler import user_router
from .cart_products.handler import card_router


router_list = [
    card_router,
    admin_router,
    user_router,
]

__all__ = [
    'router_list'
]