from enum import IntEnum, auto
from aiogram.filters.callback_data import CallbackData


class CategoryCbData(CallbackData, prefix="categ"):
    id: int
    count: int

