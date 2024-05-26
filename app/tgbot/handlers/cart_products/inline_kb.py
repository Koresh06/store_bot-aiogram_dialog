from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from app.core.models.categories import Categories

from .filter_kb import (
    CountProductsCbData,
    MenuProductsCbData,
    PaginationProductCbData,
    PagitationAction,
    ParamsProductCbData,
    ProductAction,
    QuantityAction,
    QuantutyProductCbData,
)



async def product_pagination(tg_id: int, cat_id: int, id: int, count: int):
    builder = InlineKeyboardBuilder()
    cb1 = ParamsProductCbData(action=ProductAction.add, tg_id=tg_id, id=id, cat_id=cat_id)
    cb2 = PaginationProductCbData(action=PagitationAction.back, cat_id=cat_id, id=id)
    cb3 = CountProductsCbData(value=count, cat_id=cat_id, id=id)
    cb4 = PaginationProductCbData(action=PagitationAction.forward, cat_id=cat_id, id=id)
    builder.add(InlineKeyboardButton(text='🛒 Добавить в корзину', callback_data=cb1.pack()))
    builder.row(InlineKeyboardButton(text='« Назад', callback_data=cb2.pack()),
                InlineKeyboardButton(text=f'{id}/{count}', callback_data=cb3.pack()),
                InlineKeyboardButton(text='Вперед »', callback_data=cb4.pack()))
    builder.row(
        InlineKeyboardButton(text='🛒 Корзина', callback_data='basket'),
        InlineKeyboardButton(text='⬅️ Каталог', callback_data='category'),
        width=1
    )
    return builder.as_markup()


async def updated_pagination_product(cat_id: int, id: int, quantity: int, count: int):
    print(count)
    builder = InlineKeyboardBuilder()
    cb1 = QuantutyProductCbData(action=QuantityAction.minus, id=id, cat_id=cat_id, count=count, quantity=quantity)
    cb2 = CountProductsCbData(value=count, cat_id=cat_id, id=id)
    cb3 = QuantutyProductCbData(action=QuantityAction.plus, id=id, cat_id=cat_id, count=count, quantity=quantity)
    cb4 = PaginationProductCbData(action=PagitationAction.back, cat_id=cat_id, id=id)
    cb5 = PaginationProductCbData(action=PagitationAction.forward, cat_id=cat_id, id=id)
    builder.row(
        InlineKeyboardButton(text='🔽', callback_data=cb1.pack()),
        InlineKeyboardButton(text=f'🛒 {quantity} шт.', callback_data=f"quantuty_{quantity}"),
        InlineKeyboardButton(text='🔼', callback_data=cb3.pack()),
        )
    builder.row(InlineKeyboardButton(text='« Назад', callback_data=cb4.pack()),
                InlineKeyboardButton(text=f'{id}/{count}', callback_data=cb2.pack()),
                InlineKeyboardButton(text='Вперед »', callback_data=cb5.pack()))
    builder.row(
        InlineKeyboardButton(text='🛒 Корзина', callback_data='basket'),
        InlineKeyboardButton(text='⬅️ Каталог', callback_data='category'),
        width=1
    )
        
    return builder.as_markup()


async def menu_count(cat_id: int, id: int, name_cat: list[Categories]):
    builder = InlineKeyboardBuilder()
    for count, elem in enumerate(name_cat, start=1):
        cb1 = MenuProductsCbData(cat_id=cat_id, id=count)
        if count == id:
            builder.row(
                InlineKeyboardButton(text=f'👁 🍽 {elem}', callback_data=cb1.pack())
            )
        else:
            builder.row(
                InlineKeyboardButton(text=f'🍽 {elem}', callback_data=cb1.pack())
            )
    return builder.as_markup()