
from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Multi, Jinja
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Next,
    Row,
    Select,
    Group,
    SwitchTo
)
from app.dialogs import state
from app.dialogs.callbacks import close_dialog, confirm_product, process_photo, start_categories_product

from app.dialogs.getters import get_name_categories, get_user_info


add_categories_dialog = Dialog(
    Window(
        Format('Категории товаров'),
        Group(
            Select(
                text=Format("{item.name}"),
                id='category_select',
                item_id_getter=lambda item: item.id,
                items='categories',
                on_click=start_categories_product,
            ),
            width=2   
        ),
        SwitchTo(
            Const('Добавить категорию'), 
            id='add_categories', 
            state=state.Categories.sub
        ),
        Back(Const("⬅️ Назад")),
        getter=get_name_categories,
        state=state.Categories.main
    ),
    on_process_result=close_dialog,
)


add_product  = Dialog(
    Window(
        Multi(
            Const("Введите название товара:"),
            Format("Название товара: {name}", when="name"),
            sep="\n\n",
        ),
        TextInput(id="name", on_success=Next()),
        Row(
            Cancel(Const("⬅️ Назад")),
            Next(when="name"),
        ),
        state=state.Position.name,
    ),
    Window(
        Const("Отправьте изображение товара:"),
        MessageInput(process_photo, content_types=ContentType.PHOTO),
        Row(
            Back(Const("⬅️ Назад")),
            Next(when="photo"),
        ),
        state=state.Position.photo,
    ),
    Window(
        Multi(
            Const("Введите описание товара:"),
            Format("Описание товара: {description}", when="description"),
            sep="\n\n",
        ),
        TextInput(id="description", on_success=Next()),
        Row(
            Back(Const("⬅️ Назад")),
            Next(when="description"),
        ),
        state=state.Position.description,
    ),
    Window(
        Multi(
            Const("Введите прайс товара:"),
            Format("Прайс товара: {price}", when="price"),
            sep="\n\n",
        ),
        TextInput(id="price", on_success=Next()),
        Row(
            Back(Const("⬅️ Назад")),
            Next(when="price"),
        ),
        state=state.Position.price,
    ),
    Window(
        Multi(
            Const("Подтвердите правильность данных:"),
            Format("Название: {name}!"),
            Format("Описание: {description}"),
            Format("Прайс: {price}"),
        ),
        StaticMedia(url=Jinja("{{photo}}")),
        Back(Const("⬅️ Назад")),
        Button(Const("Подтвердить"), id="confirm", on_click=confirm_product),
        state=state.Position.confirme,
        getter=get_user_info
    )
)