from aiogram.types import Message, CallbackQuery
from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from app.tgbot.dialogs.admin import state

from app.config_loader import settings
from app.core.repo.requests import RequestsRepo
from app.tgbot.handlers.admin.inline_kb import *
from app.tgbot.handlers.order_placement.filter_kb import ActionsSolutionCbData, OrderingSolutionCbDate
from app.tgbot.handlers.users.filter_kb import AdminConfirmFeetback
from app.tgbot.handlers.users.inline_kb import menu


admin_router = Router()


@admin_router.message(Command('admin'))
async def panel_admin(message: Message) -> None:
    await message.answer('Панель администратора', reply_markup=await admin_menu())


@admin_router.callback_query(F.data == 'add_position')
async def add_position(callback: CallbackQuery, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=state.Categories.main, mode=StartMode.RESET_STACK)
    

@admin_router.callback_query(OrderingSolutionCbDate.filter())
async def ordering_solution(callback: CallbackQuery, callback_data: OrderingSolutionCbDate, repo: RequestsRepo, bot: Bot):
    print(callback_data)
    if callback_data.action == ActionsSolutionCbData.ACCEPT:
        if await repo.admin.accept_status_order_user(id=callback_data.id):
            await callback.message.delete()
            await bot.send_message(chat_id=callback_data.tg_id, text=f"Ваш заказ № {callback_data.id} принят в работу!")
    else:
        if await repo.admin.reject_status_order_user(id=callback_data.id):
            await callback.message.delete()
            await bot.send_message(chat_id=callback_data.tg_id, text=f"Ваш заказ № {callback_data.id} отклонен!")
    await repo.session.commit()


@admin_router.callback_query(AdminConfirmFeetback.filter())
async def cmd_admin_confirme(callback: CallbackQuery, bot: Bot, callback_data: AdminConfirmFeetback):
    confirm = callback_data.action
    tg_id = callback_data.tg_id
    message_id = callback_data.message_id
    if confirm == 1:
        await bot.forward_message(chat_id=settings.bot.channel_id, from_chat_id=tg_id, message_id=message_id)
        await callback.answer('Отзыв подтвержден!', show_alert=True)
    else:
        await callback.answer('Отзыв отклонен!', show_alert=True, reply_markup=await menu())
        await callback.answer()
    await callback.message.delete()