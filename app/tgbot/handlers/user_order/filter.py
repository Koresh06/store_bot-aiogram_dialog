from enum import IntEnum, auto
from aiogram.filters.callback_data import CallbackData


class UserOrderListNameFilter(CallbackData, prefix="user_order_list"):
    id: int


class UserOrderDeleteFilter(CallbackData, prefix="user_order_delete"):
    id: int