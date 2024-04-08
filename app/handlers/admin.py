from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from app.dialogs import state

from app.filters.filter import Admin
from app.keyboard.inline import admin_menu


admin_router = Router()


@admin_router.message(Command('admin'), Admin())
async def panel_admin(message: Message) -> None:
    await message.answer('Панель администратора', reply_markup=await admin_menu())


@admin_router.callback_query(F.data == 'add_position')
async def add_position(callback: CallbackQuery, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=state.Categories.main, mode=StartMode.RESET_STACK)
    