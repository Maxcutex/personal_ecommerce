"""module of shopping card model class"""
from .base_model import BaseModel, db


class ShoppingCart(BaseModel):
    """shopping cart Model class"""
    __tablename__ = 'shopping_cart'

    item_id = db.Column(db.Integer(), primary_key=True)
    cart_id = db.Column(db.CHAR(32), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.product_id'), default=1)
    attributes = db.Column(db.String(1000), nullable=False)
    quantity = db.Column(db.Integer(), default=1, nullable=False)
    buy_now = db.Column(db.Boolean(), nullable=False)
    added_on = db.Column(db.DateTime(), nullable=False)

    def __str__(self):
        return '<ShoppingCart: {}>'.format(self.name)