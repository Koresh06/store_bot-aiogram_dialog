from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def admin_menu() -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='✳️ Добавить позицию', callback_data='add_position'),
        InlineKeyboardButton(text='👑 Пользователи', callback_data='users'),
        InlineKeyboardButton(text='📦 Заказы', callback_data='admin_orders'),
        InlineKeyboardButton(text='⬅️ Главное меню', callback_data='menu'),
    )

    return builder.adjust(2).as_markup()
