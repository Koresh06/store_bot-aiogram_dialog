from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from app.database.repo.requests import RequestsRepo

from app.dialogs import state
from app.keyboard.inline import admin_menu



async def start_categories_product(callback_query: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    await dialog_manager.start(state=state.Position.name, data={"category_id": item_id})
    dialog_manager.start_data['category_id'] = item_id


async def entered_name_categories(message: Message, widget: ManagedTextInput[str], dialog_manager: DialogManager, value: int,):
    repo: RequestsRepo = dialog_manager.middleware_data["repo"]
    await repo.admin.add_categories(value)
    await repo.session.commit()
    await message.answer(f"✅ Категория {value} успешно добавлена", reply_markup=await admin_menu())
    await dialog_manager.done()


async def confirm_product(callback_query: CallbackQuery, widget: Button, dialog_manager: DialogManager,):
    await callback_query.message.delete()
    repo: RequestsRepo = dialog_manager.middleware_data["repo"]
    name: TextInput = dialog_manager.find("name")
    photo = dialog_manager.dialog_data.get("photo")
    description: TextInput = dialog_manager.find("description")
    price: TextInput = dialog_manager.find("price")
    
    await repo.admin.save_product(
        {
        "tg_id": callback_query.from_user.id,
        "category_id": dialog_manager.start_data.get("category_id"),
        "name": name.get_widget_data(dialog_manager, None),
        "photo": photo,
        "description": description.get_widget_data(dialog_manager, None),
        "price": price.get_widget_data(dialog_manager, None),
        }
    )
    await repo.session.commit()
    await callback_query.message.answer("✅ Товар успешно добавлен", reply_markup=await admin_menu())

    await dialog_manager.done()


async def process_photo(message: Message, widget: Any,  dialog_manager: DialogManager,):
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data["photo"] = message.photo[-1].file_id
    await message.delete()
    await dialog_manager.next()


async def close_dialog(_, __, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.done()

