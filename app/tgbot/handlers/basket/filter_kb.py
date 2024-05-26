from aiogram.filters.callback_data import CallbackData


class EmptyBasketUserCbData(CallbackData, prefix="empty-basket"):
    tg_id: int


class DeleteProductBasketUserCbData(CallbackData, prefix="delete-product-basket"):
    id: int