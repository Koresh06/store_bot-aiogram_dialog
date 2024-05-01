from typing import Optional

from sqlalchemy import delete, select, update

from app.core.models.user import User
from app.core.models.product import Product
from app.core.models.orders import Orders
from app.core.models.cartitem import CartItem
from app.core.models.cart import Cart
from app.core.models.categories import Categories
from app.core.repo.base import BaseRepo


class UserOrderUserRepo(BaseRepo):


    async def get_user_orders(self, tg_id: int) -> Optional[dict]:
        user_d = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        stmt = await self.session.scalars(select(Orders).where(Orders.user_id == user_d.id))

        result = {}
        for num, item in enumerate(stmt, start=1):
            result[num] = item

        if result != {}:
            return result
        return False    
    

    async def get_one_order_user(self, id: int) -> Optional[dict]:
        stmt = await self.session.scalar(select(Orders).where(Orders.id == id))
        return stmt
    

    async def delete_order(self, id: int):
        await self.session.execute(delete(Orders).where(Orders.id == id))
