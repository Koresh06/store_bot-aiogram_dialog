from typing import Optional

from sqlalchemy import select

from app.core.models.categories import Categories
from app.core.models.product import Product
from app.core.models.user import User
from app.core.repo.base import BaseRepo


class AdminRepo(BaseRepo):

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
        
