from typing import Optional

from sqlalchemy import delete, select, update

from app.core.models.categories import Categories
from app.core.models.orders import Orders
from app.core.models.product import Product
from app.core.models.user import User
from app.core.repo.base import BaseRepo


class AdminRepo(BaseRepo):

    async def get_all_users(self):
        stmt = await self.session.scalars(select(User))
        return stmt

    async def get_categories(self) -> Optional[Categories]:
        categories = await self.session.scalars(select(Categories))

        if categories:
            return categories
        return False
    

    async def add_categories(self, name: str) -> Optional[Categories]:
        categories = Categories(name=name)
        self.session.add(categories)


    async def save_product(self, product: dict) -> Optional[Product]:
        user_id = await self.session.scalar(select(User.id).where(User.tg_id == product["tg_id"]))
        categori_id = await self.session.scalar(select(Categories.id).where(Categories.id == product["category_id"]))

        product = Product(user_id=user_id, categories_id=categori_id, name=product["name"], image=product["photo"], description=product["description"], price=product["price"])
        self.session.add(product)
        await self.session.execute(update(Categories).where(Categories.id == categori_id).values(count=Categories.count + 1))
        

    async def accept_status_order_user(self, id: int):
        await self.session.execute(update(Orders).where(Orders.id == id).values(status=True))
        return True


    async def reject_status_order_user(self, id: int):
        stmt = await self.session.scalar(select(Orders).where(Orders.id == id))
        await self.session.delete(stmt)
        return True
    

    async def get_all_orders(self):
        stmt = await self.session.scalars(select(Orders).where(not Orders.readiness))

        result = {}
        for num, item in enumerate(stmt, start=1):
            result[num] = item

        if result != {}:
            return result
        return False   
    

    async def get_one_order_user(self, id: int) -> Optional[dict]:
        stmt = await self.session.scalar(select(Orders).where(Orders.id == id))
        return stmt
    

    async def update_readinnes(self, id: int):
        await self.session.execute(update(Orders).where(Orders.id == id).values(readiness=True))

    
    async def get_tg_id(self, user_id: int):
        tg_id = await self.session.scalar(select(User.tg_id).where(User.id == user_id))
        return tg_id
    

    async def delete_order_user(self, id: int):
        await self.session.execute(delete(Orders).where(Orders.id == id))