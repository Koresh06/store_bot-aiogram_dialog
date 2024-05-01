from .admin.handler import admin_router
from .users.handler import user_router
from .cart_products.handler import card_router
from .basket.handler import basket_router
from .order_placement.handler import order_placement
from .user_order.handler import user_order_router


router_list = [
    user_order_router,
    order_placement,
    basket_router,
    card_router,
    admin_router,
    user_router,
]

__all__ = [
    'router_list'
]