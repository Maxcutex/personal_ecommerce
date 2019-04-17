"""empty message

Revision ID: 9d39bf6aa2d7
Revises: 
Create Date: 2019-04-17 18:54:05.096038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d39bf6aa2d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attributes',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('attribute_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('attribute_id')
    )
    op.create_table('departments',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('department_id')
    )
    op.create_table('product_attributes',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('attribute_value_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('product_id', 'attribute_value_id')
    )
    op.create_table('products',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('discounted_price', sa.Float(), nullable=False),
    sa.Column('image', sa.String(length=150), nullable=True),
    sa.Column('image2', sa.String(length=150), nullable=True),
    sa.Column('thumbnail', sa.String(length=150), nullable=True),
    sa.Column('display', sa.SmallInteger(), nullable=False),
    sa.Column('sold', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('average_rating', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('roles',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('shipping_region',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('shipping_region_id', sa.Integer(), nullable=False),
    sa.Column('shipping_region', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('shipping_region_id')
    )
    op.create_table('tax',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('tax_id', sa.Integer(), nullable=False),
    sa.Column('tax_type', sa.String(length=100), nullable=False),
    sa.Column('tax_percentage', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('tax_id')
    )
    op.create_table('attribute_values',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('attribute_value_id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=100), nullable=False),
    sa.Column('attribute_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['attribute_id'], ['attributes.attribute_id'], ),
    sa.PrimaryKeyConstraint('attribute_value_id')
    )
    op.create_table('categories',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.department_id'], ),
    sa.PrimaryKeyConstraint('category_id')
    )
    op.create_table('permissions',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('keyword', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_ratings',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('product_rating_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(length=100), nullable=True),
    sa.Column('comment', sa.String(length=1000), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('channel', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ),
    sa.PrimaryKeyConstraint('product_rating_id')
    )
    op.create_table('shipping',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('shipping_id', sa.Integer(), nullable=False),
    sa.Column('shipping_type', sa.String(length=100), nullable=False),
    sa.Column('shipping_cost', sa.Float(), nullable=False),
    sa.Column('shipping_region_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['shipping_region_id'], ['shipping_region.shipping_region_id'], ),
    sa.PrimaryKeyConstraint('shipping_id')
    )
    op.create_table('shopping_cart',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.CHAR(length=32), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('attributes', sa.String(length=1000), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('buy_now', sa.Boolean(), nullable=False),
    sa.Column('added_on', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_table('users',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('address_1', sa.String(length=100), nullable=True),
    sa.Column('address_2', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('region', sa.String(length=100), nullable=True),
    sa.Column('credit_card', sa.Text(), nullable=True),
    sa.Column('postal_code', sa.String(length=100), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('shipping_region_id', sa.Integer(), nullable=True),
    sa.Column('day_phone', sa.String(length=100), nullable=True),
    sa.Column('eve_phone', sa.String(length=100), nullable=True),
    sa.Column('mob_phone', sa.String(length=100), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.department_id'], ),
    sa.ForeignKeyConstraint(['shipping_region_id'], ['shipping_region.shipping_region_id'], ),
    sa.PrimaryKeyConstraint('customer_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('orders',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('total_amount', sa.DECIMAL(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('shipped_on', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('comments', sa.String(length=255), nullable=True),
    sa.Column('auth_code', sa.String(length=50), nullable=True),
    sa.Column('reference', sa.String(length=50), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('shipping_id', sa.Integer(), nullable=True),
    sa.Column('tax_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['users.customer_id'], ),
    sa.ForeignKeyConstraint(['shipping_id'], ['shipping.shipping_id'], ),
    sa.ForeignKeyConstraint(['tax_id'], ['tax.tax_id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('product_categories',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.category_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ),
    sa.PrimaryKeyConstraint('product_id', 'category_id')
    )
    op.create_table('user_roles',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.customer_id'], ),
    sa.PrimaryKeyConstraint('role_id', 'user_id')
    )
    op.create_table('audit',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('audit_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.PrimaryKeyConstraint('audit_id')
    )
    op.create_table('order_details',
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('attributes', sa.String(length=1000), nullable=False),
    sa.Column('product_name', sa.String(length=100), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('unit_cost', sa.DECIMAL(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_details')
    op.drop_table('audit')
    op.drop_table('user_roles')
    op.drop_table('product_categories')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('shopping_cart')
    op.drop_table('shipping')
    op.drop_table('product_ratings')
    op.drop_table('permissions')
    op.drop_table('categories')
    op.drop_table('attribute_values')
    op.drop_table('tax')
    op.drop_table('shipping_region')
    op.drop_table('roles')
    op.drop_table('products')
    op.drop_table('product_attributes')
    op.drop_table('departments')
    op.drop_table('attributes')
    # ### end Alembic commands ###
