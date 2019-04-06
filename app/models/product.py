"""module of Product model class"""
from .base_model import BaseModel, db


class Product(BaseModel):
    """Product Model class"""
    __tablename__ = 'products'

    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    price = db.Column(db.Float())
    discounted_price = db.Column(db.Float())
    image = db.Column(db.String(100))
    image2 = db.Column(db.String(100))
    thumbnail = db.Column(db.String(100))
    display = db.Column(db.Integer())

    def __str__(self):
        return self.name
