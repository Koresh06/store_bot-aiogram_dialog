from aiogram.fsm.state import State, StatesGroup


class RegisterUser(StatesGroup):
    phone = State()


class OrderPlacement(StatesGroup):
    date = State()
    method = State()


class Feetback(StatesGroup):
    text = State()
    confirm = State()