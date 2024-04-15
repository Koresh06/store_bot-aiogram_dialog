from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.types.input_media_photo import InputMediaPhoto

from app.core.repo.requests import RequestsRepo
from app.tgbot.handlers.users.inline_kb import menu
from .inline_kb import *
from .filter_kb import *


basket_router = Router()


@basket_router.callback_query(F.data == 'basket')
async def cmd_user_basket(callback: CallbackQuery, repo: RequestsRepo):
    data: dict = await repo.basket.get_basket_user(tg_id=callback.from_user.id)
    if data:
        await callback.message.delete()
        params = '\n➖➖➖➖➖➖➖➖➖➖➖\n'.join([f"|-🍽 {key}. {value['name']}\n|-{value['quantity']} шт. х {value['price']} = {value['quantity'] * value['price']} RUB" for key, value in data.items()])
        prices = sum([value['quantity'] * value['price'] for key, value in data.items()])
        await callback.message.answer(text=f"🛒 Ваша корзина:\n\n{params}\n\n💸 ИТОГО: {prices} RUB" ,reply_markup=await bascket_user_menu(tg_id=callback.from_user.id, data=data))
    else:
        await callback.answer(text=f"Ваша корзина пуста", show_alert=True)

    
@basket_router.callback_query(DeleteProductBasketUserCbData.filter())
async def cmd_delete_product_basket(callback: CallbackQuery, callback_data: DeleteProductBasketUserCbData, repo: RequestsRepo):
    if await repo.basket.delete_product_basket(tg_id=callback.from_user.id, id=callback_data.id):
        data: dict = await repo.basket.get_basket_user(tg_id=callback.from_user.id)
        if data:
            params = '\n➖➖➖➖➖➖➖➖➖➖➖\n'.join([f"|-🍽 {key}. {value['name']}\n|-{value['quantity']} шт. х {value['price']} = {value    ['quantity'] * value['price']} RUB" for key, value in data.items()])
            prices = sum([value['quantity'] * value['price'] for key, value in data.items()])
            await callback.message.edit_text(text=f"🛒 Ваша корзина:\n\n{params}\n\n💸 ИТОГО: {prices} RUB" ,reply_markup=await  bascket_user_menu(tg_id=callback.from_user.id, data=data))
        else:
            await callback.answer(text=f"Ваша корзина пуста", show_alert=True)
            await callback.message.delete()
            await callback.message.answer('Магазин бот изготовлению тортов на заказ, выберете пункт меню или воспользуйтесь командой /help', reply_markup=await menu())
    else:
        await callback.message.edit_text(text="Такого товара нет в корзине")


@basket_router.callback_query(EmptyBasketUserCbData.filter())
async def cmd_empty_basket(callback: CallbackQuery, callback_data: EmptyBasketUserCbData, repo: RequestsRepo):
    if await repo.basket.delete_basket_cart_user(tg_id=callback.from_user.id):
        await callback.answer(text="Ваша корзина очищена")
        await callback.message.delete()
        await callback.message.answer('Магазин бот изготовлению тортов на заказ, выберете пункт меню или воспользуйтесь командой /help', reply_markup=await menu())