"""module of Product model class"""
from .base_model import BaseModel, db


class Product(BaseModel):
    """Product Model class"""
    __tablename__ = 'product'

    product_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    discounted_price = db.Column(db.Float(), nullable=False, default=0.0)
    image = db.Column(db.String(150))
    image_2 = db.Column(db.String(150))
    thumbnail = db.Column(db.String(150))
    display = db.Column(db.SmallInteger(), nullable=False)
    sold = db.Column(db.Integer())
    average_rating = db.Column(db.Float, default=0.0, nullable=True)
    ratings = db.relationship('ProductRating', lazy=True)

    def __str__(self):
        return '<Product: {}>'.format(self.name)
