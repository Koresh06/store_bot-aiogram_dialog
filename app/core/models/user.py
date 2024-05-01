from typing import List, TYPE_CHECKING
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base

if TYPE_CHECKING:
    from app.core.models.orders import Orders
    from app.core.models.cart import Cart
    from app.core.models.cartitem import CartItem
    # from app.core.models.collecting_cake import Collecting_cake


class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String())
    phone: Mapped[str] = mapped_column(String())

    cart_user: Mapped['Cart'] = relationship(back_populates='user_rel', cascade='all, delete')
    order_rel: Mapped[List['Orders']] = relationship(back_populates='user_rel', cascade='all, delete')
    # collecting_rel: Mapped[List['Collecting_cake']] = relationship(back_populates='user_rel', cascade='all, delete')

    def __repr__(self) -> str:
       return f"User(id={self.id!r}, tg_id={self.tg_id!r}, username={self.username!r})"
    
    # def __str__(self) -> str:
    #     return str(self)