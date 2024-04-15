from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base


if TYPE_CHECKING:
    from app.core.models.user import User
    from app.core.models.cart import Cart


class Collecting_cake(Base):

    __tablename__ = 'collecting_cake'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id', ondelete='CASCADE'))
    event: Mapped[str] = mapped_column(String())
    image: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    date: Mapped[str] = mapped_column(String())

    user_rel: Mapped['User'] = relationship(back_populates='collecting_rel')
    cart_rel: Mapped['Cart'] = relationship(back_populates='collecting_rel')

    def __repr__(self) -> str:
        return F"Collecting_cake(id={self.id!r}, user_id={self.user_id!r}, cart_id={self.cart_id!r}, event={self.event!r}, image={self.image!r}, description={self.description!r}, data={self.date!r})"
    
    def __str__(self):
        return str(self)
