"""module of shopping card model class"""
from .base_model import BaseModel, db


class ShoppingCart(BaseModel):
    """shopping cart Model class"""
    __tablename__ = 'shopping_cart'

    cart_id = db.Column(db.String(100))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'), default=1)
    attributes = db.Column(db.String(100))

    def __str__(self):
        return self.name