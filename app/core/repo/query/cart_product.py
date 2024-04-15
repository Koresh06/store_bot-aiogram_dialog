from typing import Optional

from sqlalchemy import delete, select, update

from app.core.models.user import User
from app.core.models.product import Product
from app.core.models.cartitem import CartItem
from app.core.models.cart import Cart
from app.core.models.categories import Categories
from app.core.repo.base import BaseRepo


class CartProductRepo(BaseRepo):

    async def get_params_product(self, id: int) -> list[Product]:
        stmt = await self.session.execute(select(Product).where(Product.categories_id == id))
        result = stmt.scalars()
        
        return {item.id: {
            "id": item.id,
            "name": item.name,
            "image": item.image,
            "description": item.description,
            "price": item.price
        } for item in result}
    

    async def add_cart_user_product(self, tg_id: int, id: int) -> CartItem:
        user = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        cart_d = await self.session.scalar(select(Cart).where(Cart.user_id == user.id))
        check_cartitem = await self.session.scalar(select(CartItem).where(CartItem.cart_id == cart_d.id, CartItem.product_id == id))
        if not check_cartitem:
            self.session.add(CartItem(cart_id=cart_d.id, product_id=id))
            await self.session.commit()
            return True
        return False


    async def get_quantity_product(self, id: int) -> int:
        stmt = await self.session.scalar(select(CartItem).where(CartItem.product_id == id))
        return stmt.quantuty
    

    async def minus_quantity_product(self, tg_id: int, id: int):
        user_d = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        cart_d = await self.session.scalar(select(Cart).where(Cart.user_id == user_d.id))
        quantuti = await self.session.scalar(select(CartItem).where(CartItem.product_id == id, CartItem.cart_id == cart_d.id))

        if quantuti.quantuty > 1:
            quantuti.quantuty -= 1
            await self.session.execute(update(CartItem).where(CartItem.product_id == id, CartItem.cart_id == cart_d.id).values(quantuty=quantuti.quantuty))
            return True
        

    async def cmd_plus_cartitem_user(self, tg_id: int, id: int):
        user_d = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        cart_d = await self.session.scalar(select(Cart).where(Cart.user_id == user_d.id))
        quantuti = await self.session.scalar(select(CartItem).where(CartItem.product_id == id, CartItem.cart_id == cart_d.id))

        if quantuti.quantuty >= 5:
            return False
        quantuti.quantuty += 1
        await self.session.execute(update(CartItem).where(CartItem.product_id == id, CartItem.cart_id == cart_d.id).values(quantuty=quantuti.quantuty))
        return True


    async def delete_product_cart(self, tg_id: int, id: int):
        user_d = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        cart_d = await self.session.scalar(select(Cart).where(Cart.user_id == user_d.id))
        await self.session.execute(delete(CartItem).where(CartItem.product_id == id, CartItem.cart_id == cart_d.id))


    async def get_product_category(self, cat_id: int) -> list[Product]:
        return await self.session.scalars(select(Product.name).where(Product.categories_id == cat_id))
       
