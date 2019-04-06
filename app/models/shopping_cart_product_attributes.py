"""module of shopping cart product attributesmodel class"""
from .base_model import BaseModel, db


class ShoppingCartProductAttribute(BaseModel):
    """shopping cart product attributes Model class"""
    __tablename__ = 'shopping_cart_product_attributes'

    cart_id = db.Column(db.String(100))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'), default=1)
    product_attributes_id = db.Column(db.Integer(), db.ForeignKey('products.id'), default=1)

    def __str__(self):
        return self.name