from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.core.models.orders import Orders
from app.tgbot.handlers.user_order.filter import (
    UserOrderDeleteFilter, 
    UserOrderListNameFilter,
)


async def user_order_inline_kb(params: Orders) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for key, value in params.items():
        cb1 = UserOrderListNameFilter(id=value.id)
        builder.add(InlineKeyboardButton(text=f"#{value.id} - {value.data_time}", callback_data=cb1.pack()))
    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="menu"))

    return builder.adjust(1).as_markup()


async def user_order_delete(id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    cb1 = UserOrderDeleteFilter(id=id)
    builder.row(
        InlineKeyboardButton(text="❌ Отменить", callback_data=cb1.pack()),
        InlineKeyboardButton(text="⬅️ Назад", callback_data="orders"),
        width=1
    )
    return builder.as_markup()


