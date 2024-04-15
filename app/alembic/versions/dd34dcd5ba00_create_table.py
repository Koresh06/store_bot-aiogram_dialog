"""create table

Revision ID: dd34dcd5ba00
Revises: 
Create Date: 2024-04-13 22:57:31.590205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd34dcd5ba00'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__categories')),
    sa.UniqueConstraint('name', name=op.f('uq__categories__name'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=True),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__user'))
    )
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('cart_user_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__cart'))
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('categories_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['categories_id'], ['categories.id'], name=op.f('product_categories_id_fkey'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('product_user_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__product'))
    )
    op.create_table('cartitem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantuty', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['cart.id'], name=op.f('cartitem_cart_id_fkey'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name=op.f('cartitem_product_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__cartitem'))
    )
    op.create_table('collecting_cake',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=False),
    sa.Column('event', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('date', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['cart.id'], name=op.f('collecting_cake_cart_id_fkey'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('collecting_cake_user_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__collecting_cake'))
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=False),
    sa.Column('data_time', sa.String(), nullable=False),
    sa.Column('order', sa.JSON(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['cart.id'], name=op.f('orders_cart_id_fkey'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('orders_user_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__orders'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_table('collecting_cake')
    op.drop_table('cartitem')
    op.drop_table('product')
    op.drop_table('cart')
    op.drop_table('user')
    op.drop_table('categories')
    # ### end Alembic commands ###