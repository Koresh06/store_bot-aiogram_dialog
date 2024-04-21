from enum import IntEnum, auto
from aiogram.filters.callback_data import CallbackData


class CalendarCbData(CallbackData, prefix="calendar"):
    year: int
    month: int



class DayCalendarCbData(CallbackData, prefix="day"):
    year: int
    month: int
    day: str


class MethodPaymantCbData(CallbackData, prefix="method"):
    method: str