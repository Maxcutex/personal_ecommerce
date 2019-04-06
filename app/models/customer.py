"""module of attribute model class"""
from .base_model import BaseModel, db


class Customer(BaseModel):
    """Customer Model class"""
    __tablename__ = 'customers'

    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    address_1 = db.Column(db.String(100))
    address_1 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    region = db.Column(db.String(100))
    postal_code = db.Column(db.String(100))
    country = db.Column(db.String(100))
    shipping_region_id = db.Column(db.String(100))
    day_phone = db.Column(db.String(100))
    eve_phone = db.Column(db.String(100))
    mob_phone = db.Column(db.String(100))

    def __str__(self):
        return self.name
