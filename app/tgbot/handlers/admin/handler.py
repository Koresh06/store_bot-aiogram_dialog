from aiogram.types import Message, CallbackQuery
from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from app.tgbot.dialogs.admin import state

from app.core.repo.requests import RequestsRepo
from app.tgbot.handlers.admin.inline_kb import *
from app.tgbot.handlers.order_placement.filter_kb import ActionsSolutionCbData, OrderingSolutionCbDate


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