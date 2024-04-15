from typing import List, TYPE_CHECKING
from sqlalchemy import  Float, ForeignKey,String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base


if TYPE_CHECKING:
    from app.core.models.cartitem import CartItem
    from app.core.models.categories import Categories


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    categories_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String())
    image: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    price: Mapped[float] = mapped_column(Float())

    cartitem_rel: Mapped[List['CartItem']] = relationship(back_populates='product_rel', cascade='all, delete')
    categories_rel: Mapped['Categories'] = relationship(back_populates='product_rel')

    def __repr__(self) -> str:
       return f"Product(id={self.id!r}, user_id={self.user_id!r}, categories_id={self.categories_id!r}, name={self.name!r}, image={self.image!r}, description={self.description!r}, price={self.price!r})"
    
    # def __str__(self):
    #     return str(self)