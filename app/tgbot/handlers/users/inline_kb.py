from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.core.models.product import Product
from app.core.models.categories import Categories
from app.config_loader import settings
from .filter_kb import CategoryCbData


async def menu() -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='📋 Меню', callback_data='category'),
        InlineKeyboardButton(text='🛒 Корзина', callback_data='basket'),
        InlineKeyboardButton(text='📰 Мой Профиль', callback_data='profile'),
        InlineKeyboardButton(text='📍 Мои заказы', callback_data='orders'),
        InlineKeyboardButton(text='❓ FAQ', callback_data='faq'),
        InlineKeyboardButton(text='💬 Отзывы', callback_data='testimonials'),
    )

    return builder.adjust(2).as_markup()


async def new_user(tg_id, first_name):
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text=f'{first_name}',url=f'tg://user?id={tg_id}'))
    return builder.as_markup()


async def categories_menu(data: list[Categories]):
    builder = InlineKeyboardBuilder()

    for item in data:
        builder.row(InlineKeyboardButton(text=item.name, callback_data=CategoryCbData(id=item.id, count=item.count).pack()))
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='menu'))
    return builder.as_markup()


kb_help = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Администратор', url=f'{settings.bot.admin_id}')]
    ]
)

back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⬅️ Назад', callback_data='menu')]
    ]
)