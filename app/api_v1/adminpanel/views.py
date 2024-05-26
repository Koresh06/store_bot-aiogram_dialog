from fastapi import FastAPI, Response
from sqladmin import Admin, ModelView
from app.core.models.cartitem import CartItem

from app.core.models.user import User
from app.core.models.product import Product
# from app.core.models.collecting_cake import Collecting_cake

from app.core.session import create_engine_db
from app.config_loader import settings



app = FastAPI()

engine = create_engine_db(settings.db)
admin = Admin(app, engine=engine)


@app.get("/")
async def root(response: Response):
    return "Hello, World!"



class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.tg_id, User.username, User.phone]
    # column_details_exclude_list = [User.cart_user, User.order_rel]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"


class CartItemAdmin(ModelView, model=CartItem):
    column_list = [CartItem.id, CartItem.cart_id, CartItem.product_id, CartItem.quantuty]
    name = "Корзина"
    name_plural = "Корзины"


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.categories_rel, Product.name, Product.price, Product.description, Product.image]
    name = "Товар"
    name_plural = "Товары"
    

admin.add_view(UserAdmin)
admin.add_view(CartItemAdmin)
admin.add_view(ProductAdmin)
