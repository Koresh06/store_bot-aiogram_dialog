from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from app.core.repo.requests import RequestsRepo
from app.tgbot.dialogs.user import state


async def start_categories_user(callback_query: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    await dialog_manager.start(state=state.Catalog.types, data={"categories_id": item_id})


async def add_product_cart(callback_query: CallbackQuery, widget: Button, dialog_manager: DialogManager,):
    pass