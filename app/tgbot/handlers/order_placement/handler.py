import datetime
from aiogram import F, Router ,Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.config_loader import settings
from app.core.repo.requests import RequestsRepo
from app.tgbot.fsm.state import OrderPlacement
from .inline_kb import *
from .filter_kb import *


order_placement = Router()


@order_placement.callback_query(F.data == "order")
async def cmt_order_placement_user(callback: CallbackQuery, state: FSMContext):
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    current_date = now.date()
    await callback.message.edit_text('🗓 Укажите дату торжества, к которой необходим торт', reply_markup=await generate_calendar_markup(current_year, current_month, current_date))
    await state.set_state(OrderPlacement.date)


@order_placement.callback_query(CalendarCbData.filter())
async def process_calendar_callback(callback: CallbackQuery, callback_data: CalendarCbData):
    year, month = callback_data.year, callback_data.month
    if 0 < int(month) < 13:
        current_date = datetime.datetime.now().date()
        markup = await generate_calendar_markup(int(year), int(month), current_date)

        await callback.bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=markup)
    else:
        await callback.answer('Вы пытаетесь выйти за пределы текущего года!')


@order_placement.callback_query(DayCalendarCbData.filter(), StateFilter(OrderPlacement.date))
async def process_day_callback(callback: CallbackQuery, callback_data: DayCalendarCbData, state: FSMContext):
    if not "🔒" in callback_data.day and callback_data.day != " ":
        print(callback_data)
        year, month, day = callback_data.year, callback_data.month, callback_data.day
        selected_date = f"{day}.{month}.{year}"
        await state.update_data(date=selected_date)
        await callback.answer(f'Дата доставки установлена на {selected_date}. Спасибо!', show_alert=True)
        await callback.message.edit_text('Выберите способ оплаты', reply_markup=await method_paymant())
        await state.set_state(OrderPlacement.method)
    else:
        await callback.answer('Данную дату нельзя выбрать')


@order_placement.callback_query(MethodPaymantCbData.filter(), StateFilter(OrderPlacement.method))
async def process_method_callback(callback: CallbackQuery, callback_data: MethodPaymantCbData, state: FSMContext, repo: RequestsRepo, bot: Bot):
    await state.update_data(method=callback_data.method)
    if callback_data.method == "card":
        await callback.answer(f'Оплата картой. Находиться в разработке!')
    else:
        data = await state.get_data()
        products = await repo.order_payment.get_products_in_cart(tg_id=callback.from_user.id)
        price_order = sum([value["price"] * value["quantity"] for key, value in products.items()])
        order_id = await repo.order_payment.create_order(tg_id=callback.from_user.id, data=data, products=products, price_order=price_order)
        content = "\n".join([f'{value["description"]}: {value["quantity"]} шт.' for _, value in products.items()])
        if order_id:
            await repo.session.commit()
            await callback.message.delete()
            await bot.send_message(chat_id=settings.bot.admin_id, text=f'Новый заказ №{order_id} от {callback.from_user.first_name}\n\nДата готовности: {data["date"]}\n\nПозиции: {content}\n\n💸 ОБЩАЯ СТОИМОСТЬ: {price_order} RUB\n\n♻️ СТАТУС ОПЛАТЫ: ❌', reply_markup=await ordering_solution(id=order_id, tg_id=callback.from_user.id))
            await callback.message.answer("Ваш заказ успешно оформлен, ожидайте подтверждение администратора!\n\nГлавное меню - /start")
        else:
            await callback.message.answer("Произошла ошибка при оформлении заказа!\n\nГлавное меню - /start")