import calendar
import datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from .filter_kb import (
    CalendarCbData,
    DayCalendarCbData,
    MethodPaymantCbData,
    OrderingSolutionCbDate,
    ActionsSolutionCbData,
)


async def generate_calendar_markup(year, month, current_date):
    month_days = await generate_calendar(year, month, current_date)

    markup = InlineKeyboardBuilder()

    for week in month_days:
        for day in week:
            if day[0] == "🔒":
                cb1 = DayCalendarCbData(year=year, month=month, day=day)
                markup.add(InlineKeyboardButton(text=day, callback_data=cb1.pack()))
            else: 
                cb1 = DayCalendarCbData(year=year, month=month, day=day)
                markup.add(InlineKeyboardButton(text=day, callback_data=cb1.pack()))
    markup.adjust(7)
    cb2 = CalendarCbData(year=year, month=month - 1)
    cb3 = CalendarCbData(year=year, month=month + 1)
    markup.row(InlineKeyboardButton(text='◀️', callback_data=cb2.pack()),
               InlineKeyboardButton(text=f"{calendar.month_name[month]} {year}", callback_data="ignore"),
               InlineKeyboardButton(text='▶️', callback_data=cb3.pack()))
    
    return markup.as_markup()


async def generate_calendar(year, month, current_date):
    cal = calendar.monthcalendar(year, month)
    month_days = []

    for week in cal:
        week_days = []
        for day in week:
            if day == 0:
                week_days.append(" ")
            elif datetime.date(year, month, day) <= current_date:
                week_days.append(f"🔒 {day}")
            else:
                week_days.append(str(day))
        month_days.append(week_days)

    return month_days


async def method_paymant():
    builder = InlineKeyboardBuilder()

    cb1 = MethodPaymantCbData(method="card")
    cb2 = MethodPaymantCbData(method="cash")
    builder.row(
        InlineKeyboardButton(text='💳 Оплатить сейчас', callback_data=cb1.pack()),
        InlineKeyboardButton(text='🎁 Оплатить после получения заказа', callback_data=cb2.pack())
    )
    builder.adjust(1)
    return builder.as_markup()


async def ordering_solution(id, tg_id):
    builder = InlineKeyboardBuilder()

    cb1 = OrderingSolutionCbDate(action=ActionsSolutionCbData.ACCEPT, id=id, tg_id=tg_id)
    cb2 = OrderingSolutionCbDate(action=ActionsSolutionCbData.REJECT, id=id, tg_id=tg_id)
    builder.add(InlineKeyboardButton(text='Принять заказ', callback_data=cb1.pack()))
    builder.add(InlineKeyboardButton(text='Отклонить', callback_data=cb2.pack()))

    return builder.as_markup()