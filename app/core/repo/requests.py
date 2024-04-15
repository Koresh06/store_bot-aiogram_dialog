from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.repo.query.cart_product import CartProductRepo

from app.core.repo.query.user import UserRepo
from app.core.repo.query.admin import AdminRepo
from app.core.repo.query.basket import BasketUserRepo


@dataclass
class RequestsRepo:

    session: AsyncSession


    @property
    def users(self) -> UserRepo:
        
        return UserRepo(self.session)


    @property
    def admin(self) -> AdminRepo:
        
        return AdminRepo(self.session)
    

    @property
    def cart_product(self) -> CartProductRepo:
        
        return CartProductRepo(self.session)
    

    @property
    def basket(self) -> BasketUserRepo: 
        
        return BasketUserRepo(self.session)
   