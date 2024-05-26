from aiogram_dialog import DialogManager

from app.core.repo.requests import RequestsRepo


async def get_all_products(dialog_manager: DialogManager, repo: RequestsRepo, **kwargs):
    products = await repo.users.get_products()
    res =  {"products": [i for i in products]}
    print(res)
    return res


    