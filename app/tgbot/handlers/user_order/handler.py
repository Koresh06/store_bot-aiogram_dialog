from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.core.repo.requests import RequestsRepo
from app.tgbot.handlers.user_order.inline_kb import *
from app.tgbot.handlers.user_order.filter import *



user_order_router = Router()


@user_order_router.callback_query(F.data == 'orders')
async def user_orders(callback: CallbackQuery, repo: RequestsRepo):
    orders = await repo.user_order.get_user_orders(tg_id=callback.from_user.id)
    await callback.message.edit_text(text="Ваши заказы: ", reply_markup=await user_order_inline_kb(params=orders))
    await repo.session.commit()


@user_order_router.callback_query(UserOrderListNameFilter.filter())
async def get_order_position(callback: CallbackQuery, callback_data: UserOrderListNameFilter, repo: RequestsRepo):
    order: Orders = await repo.user_order.get_one_order_user(id=callback_data.id)
    content = "\n".join([f'{key} - {value["name"]}: {value["quantity"]} шт.' for key, value in order.order.items()])
    await callback.message.edit_text(text=f"Заказ №{callback_data.id}:\n\nДата готовности: {order.data_time}\n\nПозиции: \n{content}\n\n💸 Общая стоимость: {order.price} RUB\n\n♻️ СТАТУС ОПЛАТЫ: {'✅' if order.method == 'cash' else '❌'}", reply_markup=await user_order_delete(id=callback_data.id))


@user_order_router.callback_query(UserOrderDeleteFilter.filter())
async def delete_order(callback: CallbackQuery, callback_data: UserOrderDeleteFilter, repo: RequestsRepo):
    await repo.user_order.delete_order(id=callback_data.id)
    await callback.answer(text=f"Заказ #{callback_data.id} удален")
    orders = await repo.user_order.get_user_orders(tg_id=callback.from_user.id)
    await callback.message.edit_text(text="Ваши заказы: ", reply_markup=await user_order_inline_kb(params=orders))
    await repo.session.commit()