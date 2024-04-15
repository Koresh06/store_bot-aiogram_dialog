from typing import Optional

from sqlalchemy import delete, select, update

from app.core.models.user import User
from app.core.models.product import Product
from app.core.models.cartitem import CartItem
from app.core.models.cart import Cart
from app.core.models.categories import Categories
from app.core.repo.base import BaseRepo


class BasketUserRepo(BaseRepo):


    async def get_basket_user(self, tg_id: int):
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
    

    async def delete_product_basket(self, tg_id: int, id: int):
        user_d = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        cart_d = await self.session.scalar(select(Cart).where(Cart.id == user_d.id))
        stmt = await self.session.scalar(select(CartItem).where(CartItem.cart_id == cart_d.id, Product.id == id))
        if stmt.quantuty > 1:
            await self.session.execute(update(CartItem).where(CartItem.product_id == id, CartItem.cart_id == cart_d.id).values(quantuty=stmt.quantuty - 1)) 
            await self.session.commit()   
            return True        
        else:
            await self.session.delete(stmt)
            await self.session.commit()
            return True

    
    async def delete_basket_cart_user(self, tg_id: int):
        user_d = await self.session.scalar(select(User).where(User.tg_id == tg_id))
        cart_d = await self.session.scalar(select(Cart).where(Cart.id == user_d.id))
        cartitem_d = await self.session.scalars(select(CartItem).where(CartItem.cart_id == cart_d.id))
        for item in cartitem_d:
            await self.session.delete(item)
        await self.session.commit()
        return True