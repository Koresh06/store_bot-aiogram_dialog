from typing import List
from sqlalchemy import JSON, BigInteger, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base


class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String())
    phone: Mapped[str] = mapped_column(String())

    cart_user: Mapped[List['Cart']] = relationship(back_populates='user_rel', cascade='all, delete')
    order_rel: Mapped[List['Orders']] = relationship(back_populates='user_rel', cascade='all, delete')
    collecting_rel: Mapped[List['Collecting_cake']] = relationship(back_populates='user_rel', cascade='all, delete')

    def __repr__(self) -> str:
       return f"User(id={self.id!r}, tg_id={self.tg_id!r}, username={self.username!r})"
    

class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String())
    count: Mapped[int] = mapped_column(Integer(), default=0)

    product_rel: Mapped[List['Product']] = relationship(back_populates='categories_rel', cascade='all, delete')   

    def __repr__(self) -> str:
       return f"Categories(id={self.id!r}, name={self.name!r}, count={self.count!r})"


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
       

class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))

    user_rel: Mapped['User'] = relationship(back_populates='cart_user')
    items: Mapped[List['CartItem']] = relationship(back_populates='cart_rel', cascade='all, delete')
    order_rel: Mapped[List['Orders']] = relationship(back_populates='cart_rel', cascade='all, delete')
    collecting_rel: Mapped[List['Collecting_cake']] = relationship(back_populates='cart_rel', cascade='all, delete')

    def __repr__(self) -> str:
       return f"Cart(id={self.id!r}, user_id={self.user_id!r})"
        


class CartItem(Base):
    __tablename__ = 'cartitem'

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'))
    quantuty: Mapped[int] = mapped_column(default=1)

    cart_rel: Mapped['Cart'] = relationship(back_populates='items')
    product_rel: Mapped['Product'] = relationship(back_populates='cartitem_rel')

    def __repr__(self) -> str:
       return f"CartItem(id={self.id!r}, cart_id={self.cart_id!r}, product_id={self.product_id!r}, quantuty={self.quantuty!r})"
    

class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id', ondelete='CASCADE'))
    data_time: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column(String())
    order: Mapped[dict] = mapped_column(JSON())
    total_cost: Mapped[float] = mapped_column(Float())
    # status: Mapped[bool] = mapped_column(default=False)
    # readiness: Mapped[bool] = mapped_column(default=False)
    # obtaining: Mapped[bool] = mapped_column(default=False)

    user_rel: Mapped['User'] = relationship(back_populates='order_rel')
    cart_rel: Mapped['Cart'] = relationship(back_populates='order_rel')

    def __repr__(self) -> str:
        return f"Orders(id={self.id!r}, user_id={self.user_id!r}, cart_id={self.cart_id!r}, data_time={self.data_time!r}, address={self.address!r}, order={self.order!r}, total_cost={self.total_cost!r})"


class Collecting_cake(Base):

    __tablename__ = 'collecting_cake'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id', ondelete='CASCADE'))
    event: Mapped[str] = mapped_column(String())
    image: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    data: Mapped[str] = mapped_column(String())
    address: Mapped[str] = mapped_column(String())
    # readiness: Mapped[bool] = mapped_column(default=False)
    # obtaining: Mapped[bool] = mapped_column(default=False)

    user_rel: Mapped['User'] = relationship(back_populates='collecting_rel')
    cart_rel: Mapped['Cart'] = relationship(back_populates='collecting_rel')

    def __repr__(self) -> str:
        return F"Collecting_cake(id={self.id!r}, user_id={self.user_id!r}, cart_id={self.cart_id!r}, event={self.event!r}, image={self.image!r}, description={self.description!r}, data={self.data!r}, address={self.address!r})"
