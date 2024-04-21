from typing import Optional

from sqlalchemy import delete, select, update

from app.core.models.user import User
from app.core.models.product import Product
from app.core.models.cartitem import CartItem
from app.core.models.cart import Cart
from app.core.models.categories import Categories
from app.core.models.orders import Orders
from app.core.repo.base import BaseRepo


class OrderPaymentRepo(BaseRepo):

    async def get_products_in_cart(self, tg_id: int):
        user_d = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        cart_d = await self.session.scalar(select(Cart).where(Cart.id == user_d.id))
        stmt = await self.session.scalars(select(CartItem).where(CartItem.cart_id == cart_d.id))

        result = {}
        for num, item in enumerate(stmt, start=1):
            param = await self.session.scalar(select(Product).where(Product.id == item.product_id))
            result[num] = {
                "id": param.id,
                "name": param.name,
                "image": param.image,
                "description": param.description,
                "price": param.price,
                "quantity": item.quantuty,
            }
        if result != {}:
            return result
        return False
    

    async def create_order(self, tg_id: int, data: dict, products: dict):
        user_d = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        cart_d = await self.session.scalar(select(Cart).where(Cart.id == user_d.id))
        print(data["date"], data["method"])

        price_order = sum([value["price"] * value["quantity"] for key, value in products.items()])

        self.session.add(Orders(user_id=user_d.id, cart_id=cart_d.id, data_time=data["date"], order=products, price=price_order, method=data["method"]))

        cartitem_d = await self.session.scalars(select(CartItem).where(CartItem.cart_id == cart_d.id))
        for item in cartitem_d:
            await self.session.delete(item)

        return True