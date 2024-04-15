from aiogram.fsm.state import State, StatesGroup


class RegisterUser(StatesGroup):
    phone = State()