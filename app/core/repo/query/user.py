from typing import Optional

from sqlalchemy import select
from app.core.models.cart import Cart

from app.core.models.user import User
from app.core.models.product import Product
from app.core.models.categories import Categories
from app.core.repo.base import BaseRepo


class UserRepo(BaseRepo):


    async def add_user(self, tg_id: int, username: str, phone: str):
        self.session.add(User(tg_id=tg_id, username=username, phone=phone))
        self.session.add(Cart(user_id=tg_id))
        return True


    async def check_user(self, tg_id: int) -> Optional[User]:
        user = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            return True
        return False
    

    # async def get_products(self) -> list[Product]:
    #     stmt = await self.session.scalars(select(Product))
        
    #     if not stmt:
    #         return []
    #     return stmt


    async def get_categories_name(self) -> list[Categories]:
        stmt = await self.session.scalars(select(Categories))
        
        if not stmt:
            return False
        return stmt
    

    async def show_phone(self, tg_id: int) -> Optional[str]:
        user = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        return user.phone