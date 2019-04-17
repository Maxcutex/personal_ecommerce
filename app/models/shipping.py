"""module of shipping model class"""
from .base_model import BaseModel, db


class Shipping(BaseModel):
    """shipping Model class"""
    __tablename__ = 'shipping'

    shipping_type = db.Column(db.String(100), nullable=False)
    shipping_cost = db.Column(db.Float(), nullable=False)
    shipping_region_id = db.Column(db.Integer(), db.ForeignKey('shipping_region.id'), default=1)
    shipping_region = db.relationship('ShippingRegion', lazy=False)

    def __str__(self):
        return self.name