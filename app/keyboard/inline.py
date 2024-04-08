from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton



async def menu(tg_id: int) -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='📋 Меню', callback_data='menu'),
        InlineKeyboardButton(text='🛒 Корзина', callback_data='basket'),
        InlineKeyboardButton(text='📰 Мой Профиль', callback_data='profile'),
        InlineKeyboardButton(text='📍 Мои заказы', callback_data='orders'),
        InlineKeyboardButton(text='❓ FAQ', callback_data='faq'),
        InlineKeyboardButton(text='💬 Отзывы', callback_data='testimonials'),
    )

    return builder.adjust(2).as_markup()


async def admin_menu() -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='✳️ Добавить позицию', callback_data='add_position'),
        InlineKeyboardButton(text='👑 Пользователи', callback_data='users'),
        InlineKeyboardButton(text='📦 Заказы', callback_data='admin_orders'),
        InlineKeyboardButton(text='⬅️ Главное меню', callback_data='main_menu'),
    )

    return builder.adjust(2).as_markup()
