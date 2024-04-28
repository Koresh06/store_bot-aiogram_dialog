from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base


if TYPE_CHECKING:
    from app.core.models.user import User
    from app.core.models.cartitem import CartItem
    from app.core.models.orders import Orders
    from app.core.models.collecting_cake import Collecting_cake


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))

    user_rel: Mapped['User'] = relationship(back_populates='cart_user')
    items_rel: Mapped[List['CartItem']] = relationship(back_populates='cart_rel', cascade='all, delete')
    order_rel: Mapped[List['Orders']] = relationship(back_populates='cart_rel', cascade='all, delete')
    collecting_rel: Mapped[List['Collecting_cake']] = relationship(back_populates='cart_rel', cascade='all, delete')

    def __repr__(self) -> str:
       return f"Cart(id={self.id!r}, user_id={self.user_id!r})"
    
    # def __str__(self) -> str:
    #     return str(self)