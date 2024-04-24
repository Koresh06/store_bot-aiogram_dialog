from enum import IntEnum, auto
from aiogram.filters.callback_data import CallbackData


class CategoryCbData(CallbackData, prefix="categ"):
    id: int
    count: int


class ActionConfirm(IntEnum):
    YES = auto()
    NONE = auto()


class ConfirFeetback(CallbackData, prefix="confirm"):
    action: ActionConfirm
    tg_id: int
    message_id: int


class AdminConfirmFeetback(CallbackData, prefix="admin_confirm"):
    action: ActionConfirm
    tg_id: int
    message_id: int