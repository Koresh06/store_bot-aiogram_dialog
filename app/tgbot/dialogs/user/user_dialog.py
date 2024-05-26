from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Multi, Jinja
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Next,
    Row,
    Select,
    Group
)

from app.tgbot.dialogs.user.callbacks import add_product_cart, start_categories_user
from app.tgbot.dialogs.admin.getters import get_name_categories
from app.tgbot.dialogs.user import state
from app.tgbot.dialogs.user.getters import get_all_products


catalog_dialog = Dialog(
    Window(
        Format('Категории товаров'),
        Group(
            Select(
                text=Format("{item.name}"),
                id='category_select',
                item_id_getter=lambda item: item.id,
                items='categories',
                on_click=start_categories_user,
            ),
            width=1
        ),
        Back(
            Const("⬅️ Назад"),
        ),
        getter=get_name_categories,
        state=state.Catalog.types
    ),
    Window(
        Multi(
            Const("Подтвердите правильность данных:"),
            Format("Название: {name}!"),
            Format("Описание: {description}"),
            Format("Прайс: {price}"),
        ),
        StaticMedia(url=Jinja("{{photo}}")),
        Row(
            Back(
                Const("<< Назад")
            ),
            Button(
                Const("Добавить товар"),    
                id="add_product_btn",
                on_click=add_product_cart
            ),
            Next(
                Const("Вперед >>")
            )
        ),
        state=state.Catalog.product,
        getter=get_all_products
    )
)

