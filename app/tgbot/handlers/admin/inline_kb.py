from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from app.config_loader import settings
from app.core.models.orders import Orders
from app.core.models.user import User
from app.tgbot.handlers.admin.filter_kb import (
    ActionOrderAdmin,
    AdminOrdersUsersFilter,
    ActionAdminOrdrsUser
)


async def admin_menu() -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='✳️ Добавить позицию', callback_data='add_position'),
        InlineKeyboardButton(text='👑 Пользователи', callback_data='users'),
        InlineKeyboardButton(text='📦 Заказы', callback_data='admin_orders'),
        InlineKeyboardButton(text='⬅️ Главное меню', callback_data='menu'),
    )

    return builder.adjust(2).as_markup()


async def users_name(params: User):
    builder = InlineKeyboardBuilder()

    for item in params:
        builder.add(InlineKeyboardButton(text=f"{item.username}", url=f'tg://user?id={item.tg_id}'))
    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_menu"))

    return builder.adjust(1).as_markup()


def inline_builder():
    builder = InlineKeyboardBuilder()
    builder.button(text="Admin Panel", web_app=WebAppInfo(url=settings.bot.WEBHOOK_URL))
    return builder.as_markup()

async def admin_orders_inline_kb(params: Orders) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for key, value in params.items():
        cb1 = AdminOrdersUsersFilter(id=value.id)
        builder.add(InlineKeyboardButton(text=f"#{value.id} - {value.data_time}", callback_data=cb1.pack()))
    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_menu"))

    return builder.adjust(1).as_markup()


async def admin_action_order(id: int, tg_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    cb1 = ActionAdminOrdrsUser(action=ActionOrderAdmin.CONFIRM, id=id, tg_id=tg_id)
    cb2 = ActionAdminOrdrsUser(action=ActionOrderAdmin.CANCEL, id=id, tg_id=tg_id)
    builder.row(
        InlineKeyboardButton(text="✅ Подтвердить", callback_data=cb1.pack()),
        InlineKeyboardButton(text="❌ Отменить", callback_data=cb2.pack()),
        InlineKeyboardButton(text="⬅️ Назад", callback_data="orders"),
        width=1
    )
    return builder.as_markup()
