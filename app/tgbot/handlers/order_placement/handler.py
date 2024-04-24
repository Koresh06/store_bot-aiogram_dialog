import datetime
from aiogram import F, Router, Bot, types
from aiogram.types import CallbackQuery, ContentType, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.config_loader import settings
from app.core.repo.requests import RequestsRepo
from app.tgbot.fsm.state import OrderPlacement
from app.tgbot.handlers.users.inline_kb import menu
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
    await callback.message.delete()
    await state.update_data(method=callback_data.method)
    data = await state.get_data()
    products = await repo.order_payment.get_products_in_cart(tg_id=callback.from_user.id)
    price_order = sum([value["price"] * value["quantity"] for key, value in products.items()])
    order_id = await repo.order_payment.create_order(tg_id=callback.from_user.id, data=data, products=products,price_order=price_order)
    content = "\n".join([f'{value["description"]}: {value["quantity"]} шт.' for _, value in products.items()])
    if callback_data.method == "card":
        # await callback.answer("Оплата нахожится в разработке")
        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title='Оплата корзины',
            description=content,
            provider_token=settings.bot.token_yookassa,
            payload=f'month_sub_{order_id}',
            currency='rub',
            prices=[
                types.LabeledPrice(
                    label='Руб',
                    amount=f'{price_order * 100:.2f}'

                )
            ],
            start_parameter='store',
            need_name=True,
        )
    else:
        if order_id:
            await repo.order_payment.delete_basket_product_user(tg_id=callback.from_user.id)
            await bot.send_message(chat_id=settings.bot.admin_id, text=f'Новый заказ №{order_id} от {callback.from_user.first_name}\n\nДата готовности: {data["date"]}\n\nПозиции: {content}\n\n💸 ОБЩАЯ СТОИМОСТЬ: {price_order} RUB\n\n♻️ СТАТУС ОПЛАТЫ: ❌', reply_markup=await ordering_solution(id=order_id, tg_id=callback.from_user.id))
            await callback.message.answer("✅ Ваш заказ успешно оформлен, ожидайте подтверждение администратора!", reply_markup= await menu())
        else:
            await callback.message.answer("Произошла ошибка при оформлении заказа!\n\nГлавное меню - /start")
    await state.clear()
    await callback.answer()
    await repo.session.commit()


@order_placement.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout: types.PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


@order_placement.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: Message, bot: Bot, repo: RequestsRepo):
    if message.successful_payment.invoice_payload.split('_')[0] == 'month':
        id = message.successful_payment.invoice_payload.split('_')[-1]
        await repo.order_payment.update_status_order(tg_id=message.from_user.id, id=id)
        order = await repo.order_payment.get_order_user(id=id)
        content = "\n".join([f'{value["description"]}: {value["quantity"]} шт.' for _, value in order.order.items()])
        await bot.send_message(chat_id=settings.bot.admin_id, text=f'Новый заказ №{id} от {message.from_user.first_name}\n\nДата готовности: {order.data_time}\n\nПозиции: {content}\n\n💸 ОБЩАЯ СТОИМОСТЬ: {order.price} RUB\n\n♻️ СТАТУС ОПЛАТЫ: ✅', reply_markup=await ordering_solution(id=id, tg_id=message.from_user.id))
        await message.answer("✅ Ваш заказ успешно оформлен и оплачен, ожидайте подтверждение администратора!", reply_markup= await menu())
        await repo.session.commit()


@order_placement.callback_query(OrderingSolutionCbDate.filter(F.action == ActionsSolutionCbData.ACCEPT))
async def accept_callback(callback: CallbackQuery, callback_data: OrderingSolutionCbDate, bot: Bot):
    await callback.message.delete()
    await bot.send_message(chat_id=callback_data.tg_id, text=f"✅ Заказ #{callback_data.id} принят.\nПо готовности с вами свяжется администратор\n\nГлавное меню - /start")


@order_placement.callback_query(OrderingSolutionCbDate.filter(F.action == ActionsSolutionCbData.REJECT))
async def reject_callback(callback: CallbackQuery, callback_data: OrderingSolutionCbDate, bot: Bot, repo: RequestsRepo):
    await callback.message.delete()
    await repo.order_payment.delete_order(id=callback_data.id)
    await repo.session.commit()
    await bot.send_message(chat_id=callback_data.tg_id, text=f"❌ Заказ #{callback_data.id} отклонен.\n\nГлавное меню - /start")



