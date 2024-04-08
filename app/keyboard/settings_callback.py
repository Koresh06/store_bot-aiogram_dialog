from aiogram.filters.callback_data import CallbackData


class MenuUsersCallback(CallbackData, prefix="menu_users"):
    
    foo: str
    tg_id: int