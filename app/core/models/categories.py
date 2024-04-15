from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base


if TYPE_CHECKING:
    from app.core.models.product import Product


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    count: Mapped[int] = mapped_column(Integer(), default=0)

    product_rel: Mapped[List['Product']] = relationship(back_populates='categories_rel', cascade='all, delete')   

    def __repr__(self) -> str:
       return f"Categories(id={self.id!r}, name={self.name!r}, count={self.count!r})"
    
    def __str__(self) -> str:
        return str(self)