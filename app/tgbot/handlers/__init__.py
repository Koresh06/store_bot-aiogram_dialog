from .admin.handler import admin_router
from .users.handler import user_router
from .cart_products.handler import card_router
from .basket.handler import basket_router


router_list = [
    basket_router,
    card_router,
    admin_router,
    user_router,
]

__all__ = [
    'router_list'
]