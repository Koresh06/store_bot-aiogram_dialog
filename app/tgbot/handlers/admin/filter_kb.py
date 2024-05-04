from enum import IntEnum, auto
from aiogram.filters.callback_data import CallbackData


class AdminOrdersUsersFilter(CallbackData, prefix="admin-orders-users"):
    id: int


class ActionOrderAdmin(IntEnum):
    CONFIRM = auto()
    CANCEL = auto()



class ActionAdminOrdrsUser(CallbackData, prefix="action-admin-orders-users"):
    action: ActionOrderAdmin
    id: int
    tg_id: int