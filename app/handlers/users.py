from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.database.repo.requests import RequestsRepo
from app.fsm.state import RegisterUser
from app.keyboard.inline import menu


user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message, repo: RequestsRepo, state: FSMContext) -> None:
    user = await repo.users.check_user(message.from_user.id)

    if user:
        await message.answer(f'Привет, {message.from_user.full_name}!\n\nВведи номер телефона в формате +7XXXXXXXXXX:')
        await state.set_state(RegisterUser.phone)
    else:
        await message.answer('Магазин бот изготовлению тортов на заказ, выберете пункт меню или воспользуйтесь командой /help', reply_markup=await menu(message.from_user.id))


@user_router.message(RegisterUser.phone)
async def register_phone(message: Message, repo: RequestsRepo, state: FSMContext) -> None:
    await repo.users.add_user(message.from_user.id, message.from_user.username, message.text)
    await message.answer('Вы успешно зарегистрированы!', reply_markup=await menu(message.from_user.id))
    await state.clear()
    await repo.session.commit()