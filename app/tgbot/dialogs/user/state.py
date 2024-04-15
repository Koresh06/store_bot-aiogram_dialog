from aiogram.fsm.state import State, StatesGroup


class Catalog(StatesGroup):
    types = State()
    product = State()