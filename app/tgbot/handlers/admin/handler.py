from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from app.tgbot.dialogs.admin import state

from app.tgbot.handlers.admin.inline_kb import *


admin_router = Router()


@admin_router.message(Command('admin'))
async def panel_admin(message: Message) -> None:
    await message.answer('Панель администратора', reply_markup=await admin_menu())


@admin_router.callback_query(F.data == 'add_position')
async def add_position(callback: CallbackQuery, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=state.Categories.main, mode=StartMode.RESET_STACK)
    