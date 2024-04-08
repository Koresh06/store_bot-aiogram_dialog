from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput

from app.database.repo.requests import RequestsRepo


async def get_name_categories(dialog_manager: DialogManager, repo: RequestsRepo, **kwargs):

    categories = await repo.admin.get_categories()
    return {
        "categories": [i for i in categories]
    }


async def get_user_info(dialog_manager: DialogManager, **kwargs):
    name: TextInput = dialog_manager.find("name")
    photo = dialog_manager.dialog_data.get("photo")
    description: TextInput = dialog_manager.find("description")
    price: TextInput = dialog_manager.find("price")

    return {
        "name": name.get_widget_data(dialog_manager, None),
        "photo": photo,
        "description": description.get_widget_data(dialog_manager, None),
        "price": price.get_widget_data(dialog_manager, None),
    }