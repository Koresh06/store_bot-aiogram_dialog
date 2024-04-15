from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.types.input_media_photo import InputMediaPhoto

from app.core.repo.requests import RequestsRepo
from app.tgbot.handlers.cart_products.inline_kb import *
from ..users.filter_kb import *


card_router = Router()


@card_router.callback_query(CategoryCbData.filter())
async def cart_product_one(callback: CallbackQuery, callback_data: CategoryCbData, repo: RequestsRepo) -> None:
    await callback.message.delete()
    data: dict = await repo.cart_product.get_params_product(callback_data.id)
    item = data[callback_data.id]
    await callback.message.answer_photo(item['image'], caption=f"🍰 <b><i>Наименование:</i></b> {item['name']}  \n\n🔖   <b><i>Состав/описание торта:</i></b> {item['description']}\n\n💵 <b><i>Прайс:</i></b> {item['price']} RUB за кг.", reply_markup= await product_pagination(tg_id=callback.from_user.id, cat_id=callback_data.id, id=item['id'], count=len(data)))
    await callback.answer()


@card_router.callback_query(PaginationProductCbData.filter(F.action == PagitationAction.back))
async def back_pagonation_product(callback: CallbackQuery, callback_data: PaginationProductCbData, repo: RequestsRepo) -> None:
    data: dict = await repo.cart_product.get_params_product(callback_data.cat_id)
    if callback_data.id > 1:
        value = data[callback_data.id - 1]
        await callback.message.edit_media(media=InputMediaPhoto(media=value["image"]))
        await callback.message.edit_caption(caption=f"🍰 <b><i>Наименование:</i></b> {value['name']}  \n\n🔖   <b><i>Состав/описание торта:</i></b> {value['description']}\n\n💵 <b><i>Прайс:</i></b> {value['price']} RUB за кг.", reply_markup=await product_pagination(tg_id=callback.from_user.id, cat_id=callback_data.cat_id, id=value['id'], count=len(data)))
    else:
        value = data[len(data)]
        await callback.message.edit_media(media=InputMediaPhoto(media=value["image"]))
        await callback.message.edit_caption(caption=f"🍰 <b><i>Наименование:</i></b> {value['name']}  \n\n🔖   <b><i>Состав/описание торта:</i></b> {value['description']}\n\n💵 <b><i>Прайс:</i></b> {value['price']} RUB за кг.", reply_markup=await product_pagination(tg_id=callback.from_user.id, cat_id=callback_data.cat_id, id=value['id'], count=len(data)))



@card_router.callback_query(PaginationProductCbData.filter(F.action == PagitationAction.forward))
async def forward_pagonation_product(callback: CallbackQuery, callback_data: PaginationProductCbData, repo: RequestsRepo) -> None:
    data: dict = await repo.cart_product.get_params_product(callback_data.cat_id)
    if callback_data.id < len(data):
        value = data[callback_data.id + 1]
        await callback.message.edit_media(media=InputMediaPhoto(media=value["image"]))
        await callback.message.edit_caption(caption=f"🍰 <b><i>Наименование:</i></b> {value['name']}  \n\n🔖   <b><i>Состав/описание торта:</i></b> {value['description']}\n\n💵 <b><i>Прайс:</i></b> {value['price']} RUB за кг.", reply_markup=await product_pagination(tg_id=callback.from_user.id, cat_id=callback_data.cat_id, id=callback_data.id + 1, count=len(data)))
    else:
        value = next(iter(data.values()))
        await callback.message.edit_media(media=InputMediaPhoto(media=value["image"]))
        await callback.message.edit_caption(caption=f"🍰 <b><i>Наименование:</i></b> {value['name']}  \n\n🔖   <b><i>Состав/описание торта:</i></b> {value['description']}\n\n💵 <b><i>Прайс:</i></b> {value['price']} RUB за кг.", reply_markup=await product_pagination(tg_id=callback.from_user.id, cat_id=callback_data.cat_id, id=value['id'], count=len(data)))


@card_router.callback_query(ParamsProductCbData.filter(F.action == ProductAction.add))
async def add_cart_product(callback: CallbackQuery, callback_data: ParamsProductCbData, repo: RequestsRepo) -> None:
    if await repo.cart_product.add_cart_user_product(tg_id=callback.from_user.id, id=callback_data.id):
        data: dict = await repo.cart_product.get_params_product(callback_data.cat_id)
        quantity = await repo.cart_product.get_quantity_product(callback_data.id)
        await callback.message.edit_reply_markup(reply_markup=await updated_pagination_product(cat_id=callback_data.cat_id, id=callback_data.id, quantity=quantity, count=len(data)))
    else:
        await callback.answer("Товар уже добавленвся в корзину", show_alert=True)


@card_router.callback_query(QuantutyProductCbData.filter(F.action == QuantityAction.minus))
async def cmd_minus_cartitem_user(callback: CallbackQuery, callback_data: QuantutyProductCbData, repo: RequestsRepo) -> None:
    if await repo.cart_product.minus_quantity_product(callback.from_user.id, callback_data.id):
        await repo.session.commit()
        quantity = await repo.cart_product.get_quantity_product(callback_data.id)
        await callback.message.edit_reply_markup(reply_markup=await updated_pagination_product(cat_id=callback_data.cat_id, id=callback_data.id, quantity=quantity, count=callback_data.count))
    else:
        await repo.cart_product.delete_product_cart(callback.from_user.id, callback_data.id)
        await repo.session.commit()
        await callback.message.edit_reply_markup(reply_markup=await product_pagination(tg_id=callback.from_user.id, cat_id=callback_data.cat_id, id=callback_data.id, count=callback_data.count))


@card_router.callback_query(QuantutyProductCbData.filter(F.action == QuantityAction.plus))
async def cmd_plus_catitem_user(callback: CallbackQuery, callback_data: QuantutyProductCbData, repo: RequestsRepo) -> None:
    if await repo.cart_product.cmd_plus_cartitem_user(callback.from_user.id, callback_data.id):
        await repo.session.commit()
        quantity = await repo.cart_product.get_quantity_product(callback_data.id)
        await callback.message.edit_reply_markup(reply_markup=await updated_pagination_product(cat_id=callback_data.cat_id, id=callback_data.id, quantity=quantity, count=callback_data.count))
    else:
        await callback.answer("Максимальное количество 5 шт.", show_alert=True)


@card_router.callback_query(CountProductsCbData.filter())
async def cmd_count_menu_product(callback: CallbackQuery, callback_data: CountProductsCbData, repo: RequestsRepo) -> None:
    photo = FSInputFile("menu_tovar.jpg")
    name_cat: list[Categories] = await repo.cart_product.get_product_category(callback_data.cat_id)
    await callback.message.edit_media(media=InputMediaPhoto(media=photo))
    await callback.message.edit_caption(caption='🗂|Товары', reply_markup=await menu_count(cat_id=callback_data.cat_id, id=callback_data.id, name_cat=name_cat))


@card_router.callback_query(MenuProductsCbData.filter())
async def cmd_menu_product(callback: CallbackQuery, callback_data: MenuProductsCbData, repo: RequestsRepo) -> None:
    data: dict = await repo.cart_product.get_params_product(callback_data.cat_id)
    value = data[callback_data.id]
    await callback.message.edit_media(media=InputMediaPhoto(media=value["image"]))
    await callback.message.edit_caption(caption=f"🍰 <b><i>Наименование:</i></b> {value['name']}  \n\n🔖   <b><i>Состав/описание торта:</i></b> {value['description']}\n\n💵 <b><i>Прайс:</i></b> {value['price']} RUB за кг.", reply_markup=await product_pagination(tg_id=callback.from_user.id, cat_id=callback_data.cat_id, id=value['id'], count=len(data)))


@card_router.callback_query(F.startwith("quantuty"))
async def show_quantity(callback: CallbackQuery):
    quantity = callback.data.split('_')[-1]
    await callback.answer(f'🎂 Торт {quantity} шт.')