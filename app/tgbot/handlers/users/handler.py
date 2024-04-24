from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
# from aiogram_dialog import DialogManager, StartMode

from app.core.repo.requests import RequestsRepo
from app.tgbot.fsm.state import Feetback, RegisterUser
from app.tgbot.handlers.users.inline_kb import *
from app.tgbot.handlers.users.filter_kb import *
from app.config_loader import settings

# from app.tgbot.dialogs.user.state import Catalog


user_router = Router()


@user_router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Вы не заполняете форму, поэтому невозможно воспользоваться данной командой!'
    )

@user_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Отмена действия!'
    )
    await state.clear()


@user_router.message(CommandStart())
async def cmd_start(message: Message, repo: RequestsRepo, state: FSMContext) -> None:
    user = await repo.users.check_user(message.from_user.id)

    if user:
        await message.answer(f'Привет, {message.from_user.full_name}!\n\nВведи номер телефона в формате +7XXXXXXXXXX:')
        await state.set_state(RegisterUser.phone)
    else:
        await message.answer('Магазин бот изготовлению тортов на заказ, выберете пункт меню или воспользуйтесь командой /help', reply_markup=await menu())
        

@user_router.message(RegisterUser.phone)
async def register_phone(message: Message, repo: RequestsRepo, state: FSMContext) -> None:
    await repo.users.add_user(message.from_user.id, message.from_user.username, message.text)
    await message.answer('✅ Вы успешно зарегистрированы!', reply_markup=await menu())
    await message.bot.send_message(chat_id=settings.bot.admin_id, text=f'Новый пользователь - {message.from_user.first_name}', reply_markup=await new_user(message.from_user.id, message.from_user.first_name))
    await state.clear()
    await repo.session.commit()


@user_router.callback_query(F.data == 'menu')
async def cmd_main(callback: CallbackQuery):
    await callback.message.edit_text('Магазин бот изготовлению тортов на заказ, выберете пункт меню или воспользуйтесь командой /help', reply_markup=await menu())


@user_router.callback_query(F.data == 'category')
async def cmd_menu(callback: CallbackQuery, repo: RequestsRepo) -> None:
    await callback.message.delete()
    name_categories = await repo.users.get_categories_name()
    await callback.message.answer("Категории товаров", reply_markup=await categories_menu(name_categories))


@user_router.callback_query(F.data == 'profile')
async def user_profile(callback: CallbackQuery, repo: RequestsRepo):
    user = await repo.users.show_phone(callback.from_user.id)
    count = await repo.users.get_orders_count_user(callback.from_user.id)
    await callback.message.edit_text(f'┌📰 Ваш Профиль\n├Имя: <code>{callback.from_user.first_name}</code>\n├ID: <code>{callback.from_user.id}</code>\n├Телефон: <code>{user.phone}</code>\n└Количество заказов: <code>{count} шт.</code>', reply_markup=back_menu)
    await repo.session.commit()


@user_router.callback_query(F.data == "feedback")
async def process_feedback(callback: CallbackQuery):
    await callback.message.edit_text("Отзывы размещаются в нашем телеграмм кананале🔽", reply_markup=await feedback_kb())


@user_router.callback_query(F.data == "feedback_user")
async def start_state_feedback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Напишите ваш отзыв. \n\nВАЖНО!!! отзыв может быть только текстом:\n\n❌ Отмена - /cancel")
    await state.set_state(Feetback.text)
    await callback.answer()


@user_router.message(StateFilter(Feetback.text))
async def cmd_register_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(text=f"Подтвердите ваш отзыв\n\n<i>{message.text}</i>", reply_markup=await confirm_feetback(message.from_user.id, message.message_id))
    await state.set_state(Feetback.confirm)


@user_router.callback_query(ConfirFeetback.filter(), StateFilter(Feetback.confirm))
async def cmd_confirm(callback: CallbackQuery, state: FSMContext, bot: Bot, callback_data: ConfirFeetback):
    confirm = callback_data.action
    tg_id = callback_data.tg_id
    message_id = callback_data.message_id
    data = await state.get_data()
    await callback.message.delete()
    if confirm == 1:
        await bot.send_message(chat_id=tg_id, text="Спасибо за ваш отзыв!\n\nВаш отзыв отправлен на модерацию, в ближайшее время он будет опубликован!", reply_markup=await menu())
        await bot.send_message(chat_id=settings.bot.admin_id, text=f"Новый отзыв от {callback.from_user.first_name}:\n\n{data['text']}", reply_markup=await admin_confirm_feetback(tg_id, message_id))
    else:
        await callback.message.answer("Отзыв отклонен!", reply_markup=await menu())
    await state.clear()
    await callback.answer()


@user_router.message(Command(commands='help'))
async def cmd_help(message: Message):
    await message.delete()
    await message.answer('🔸У вас возникли вопросы?\nМы с удовольствием ответим!\n', reply_markup=kb_help)