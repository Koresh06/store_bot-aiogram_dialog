from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.core.models.categories import Categories
from app.config_loader import settings
from .filter_kb import (
    AdminConfirmFeetback,
    ConfirFeetback, 
    ActionConfirm, 
    CategoryCbData,
) 


async def menu() -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='📋 Меню', callback_data='category'),
        InlineKeyboardButton(text='🛒 Корзина', callback_data='basket'),
        InlineKeyboardButton(text='📰 Мой Профиль', callback_data='profile'),
        InlineKeyboardButton(text='📍 Мои заказы', callback_data='orders'),
        InlineKeyboardButton(text='❓ FAQ', callback_data='faq'),
        InlineKeyboardButton(text='💬 Отзывы', callback_data='feedback'),
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


async def feedback_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='🔶 Наш канал', url=settings.bot.channel_url),
        InlineKeyboardButton(text='📢 Оставить отзыв', callback_data='feedback_user'),
        InlineKeyboardButton(text='⬅️ Назад', callback_data='menu'),
    )
    return builder.adjust(2).as_markup()


async def confirm_feetback(tg_id: int, message_id: int):
    builder = InlineKeyboardBuilder()

    cb1 = ConfirFeetback(action=ActionConfirm.YES, tg_id=tg_id, message_id=message_id)
    cb2 = ConfirFeetback(action=ActionConfirm.NONE, tg_id=tg_id, message_id=message_id)

    builder.add(
        InlineKeyboardButton(text="✅ Подтвердить", callback_data=cb1.pack())
    )
    builder.add(
        InlineKeyboardButton(text="❌ Отмена", callback_data=cb2.pack())
    )
    builder.adjust(2)
    return builder.as_markup()


async def admin_confirm_feetback(tg_id: int, message_id: int):
    builder = InlineKeyboardBuilder()

    cb1 = AdminConfirmFeetback(action=ActionConfirm.YES, tg_id=tg_id, message_id=message_id)
    cb2 = AdminConfirmFeetback(action=ActionConfirm.NONE, tg_id=tg_id, message_id=message_id)

    builder.add(
        InlineKeyboardButton(text="✅ Подтвердить", callback_data=cb1.pack())
    )
    builder.add(
        InlineKeyboardButton(text="❌ Отмена", callback_data=cb2.pack())
    )
    builder.adjust(2)
    return builder.as_markup()