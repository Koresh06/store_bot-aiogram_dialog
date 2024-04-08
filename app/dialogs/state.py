from aiogram.fsm.state import State, StatesGroup


class Categories(StatesGroup):
    main = State()
    sub = State()


class Position(StatesGroup):
    name = State()
    photo = State()
    description = State()
    price = State()
    confirme = State()

    