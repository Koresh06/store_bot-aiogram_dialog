from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, JSON, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base


if TYPE_CHECKING:
    from app.core.models.user import User
    from app.core.models.cart import Cart



class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id', ondelete='CASCADE'))
    data_time: Mapped[str] = mapped_column()
    order: Mapped[dict] = mapped_column(JSON())
    price: Mapped[float] = mapped_column(Float())
    method: Mapped[str] = mapped_column(String(32))
    status: Mapped[bool] = mapped_column(default=False)

    user_rel: Mapped['User'] = relationship(back_populates='order_rel')
    cart_rel: Mapped['Cart'] = relationship(back_populates='order_rel')

    def __repr__(self) -> str:
        return f"Orders(id={self.id!r}, user_id={self.user_id!r}, cart_id={self.cart_id!r}, data_time={self.data_time!r}, order={self.order!r}, price={self.price!r})"
    
    def __str__(self):
        return str(self)