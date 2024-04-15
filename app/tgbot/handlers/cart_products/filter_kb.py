from enum import IntEnum, auto
from aiogram.filters.callback_data import CallbackData


class ProductAction(IntEnum):
    add = auto()
    update = auto()
    delete = auto()


class ParamsProductCbData(CallbackData, prefix='product'):
    action: ProductAction
    tg_id: int
    id: int
    cat_id: int


class PagitationAction(IntEnum):
    back = auto()
    forward = auto()


class PaginationProductCbData(CallbackData, prefix='pagination-product'):
    action: PagitationAction
    cat_id: int
    id: int


class CountProductsCbData(CallbackData, prefix='count=product'):
    value: int
    cat_id: int
    id: int


class QuantityAction(IntEnum):
    minus = auto()
    plus = auto()


class QuantutyProductCbData(CallbackData, prefix='quantuty-product'):
    action: QuantityAction
    id: int
    cat_id: int
    count: int
    quantity: int


class MenuProductsCbData(CallbackData, prefix='menu-products'):
    cat_id: int
    id: int

