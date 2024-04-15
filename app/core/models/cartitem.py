from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base


if TYPE_CHECKING:
    from app.core.models.product import Product
    from app.core.models.cart import Cart


class CartItem(Base):
    __tablename__ = 'cartitem'

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'))
    quantuty: Mapped[int] = mapped_column(default=1)

    cart_rel: Mapped['Cart'] = relationship(back_populates='items_rel')
    product_rel: Mapped['Product'] = relationship(back_populates='cartitem_rel')

    def __repr__(self) -> str:
       return f"CartItem(id={self.id!r}, cart_id={self.cart_id!r}, product_id={self.product_id!r}, quantuty={self.quantuty!r})"
    
    def __str__(self) -> str:
        return str(self)