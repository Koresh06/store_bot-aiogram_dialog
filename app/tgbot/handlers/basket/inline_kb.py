from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from .filter_kb import (
    DeleteProductBasketUserCbData,
    EmptyBasketUserCbData,
)


async def bascket_user_menu(tg_id: int, data: dict):
    builder = InlineKeyboardBuilder()

    cb1 = EmptyBasketUserCbData(tg_id=tg_id)

    for key, value in data.items():
        cb2 = DeleteProductBasketUserCbData(id=value["id"])
        builder.row(
            InlineKeyboardButton(text=f'❌ {key}. {value["name"]}. {value["quantity"]} шт.', callback_data=cb2.pack())
        )
    builder.row(
        InlineKeyboardButton(text='❎ Очистить корзину', callback_data=cb1.pack()),
        InlineKeyboardButton(text='🚕 Оформить заказ', callback_data='order'),
        InlineKeyboardButton(text='⬅️ Главное меню', callback_data='menu'),
        width=2,
    )

    return builder.as_markup()