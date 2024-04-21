from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
# from aiogram_dialog import DialogManager, StartMode

from app.core.repo.requests import RequestsRepo
from app.tgbot.fsm.state import RegisterUser
from app.tgbot.handlers.users.inline_kb import *
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
        text='Отмена заполнения формы\n\nПри необходимости заполните форму заново'
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


@user_router.callback_query(F.data == 'main_menu')
@user_router.callback_query(F.data == 'main')
async def cmd_main(callback: CallbackQuery):
    await callback.message.edit_text('Магазин бот изготовлению тортов на заказ, выберете пункт меню или воспользуйтесь командой /help', reply_markup=await menu())


@user_router.callback_query(F.data == 'menu')
@user_router.callback_query(F.data == 'category')
async def cmd_menu(callback: CallbackQuery, repo: RequestsRepo) -> None:
    await callback.message.delete()
    name_categories = await repo.users.get_categories_name()
    await callback.message.answer("Категории товаров", reply_markup=await categories_menu(name_categories))


@user_router.message(F.text.endswith('Мой Профиль'))
async def user_profile(message: CallbackQuery, repo: RequestsRepo):
    phone = await repo.users.show_phone(message.from_user.id)
    await message.answer(f'┌📰 Ваш Профиль\n├Имя: <code>{message.from_user.first_name}</code>\n├ID: <code>{message.from_user.id}</code>\n├Телефон: <code>{phone}</code>\n└Количество заказов: <code>0 шт.</code>')


@user_router.message(F.text.endswith('Помощь'))
async def cmd_help(message: Message):
    await message.answer('🔸У вас возникли вопросы?\nМы с удовольствием ответим!\n', reply_markup=kb_help)