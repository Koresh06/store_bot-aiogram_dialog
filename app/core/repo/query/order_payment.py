import asyncio
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
    

    async def create_order(self, tg_id: int, data: dict, products: dict, price_order: float):
        user_d = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        cart_d = await self.session.scalar(select(Cart).where(Cart.id == user_d.id))


        order = Orders(user_id=user_d.id, cart_id=cart_d.id, data_time=data["date"], order=products, price=price_order, method=data     ["method"])
        self.session.add(order)
        await self.session.commit()

        cartitem_d = await self.session.scalars(select(CartItem).where(CartItem.cart_id == cart_d.id))
        for item in cartitem_d:
            await self.session.delete(item)

        return order.id


    async def get_order_user(self, id: int):
        order = await self.session.scalar(select(Orders).where(Orders.id == id))
        if order:
            return order
        return False


    async def update_status_order(self, tg_id: int, id: int):
        await self.session.execute(update(Orders).where(Orders.id == id).values(status=True))

        user_d = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        cart_d = await self.session.scalar(select(Cart).where(Cart.id == user_d.id))
        cartitem_d = await self.session.scalars(select(CartItem).where(CartItem.cart_id == cart_d.id))
        for item in cartitem_d:
            await self.session.delete(item)


    async def delete_basket_product_user(self, tg_id: int):
        user_d = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        cart_d = await self.session.scalar(select(Cart).where(Cart.id == user_d.id))
        cartitem_d = await self.session.scalars(select(CartItem).where(CartItem.cart_id == cart_d.id))
        for item in cartitem_d:
            await self.session.delete(item)



    async def delete_order(self, id: int):
        stmt = await self.session.scalar(select(Orders).where(Orders.id == id))
        await self.session.delete(stmt)

        


