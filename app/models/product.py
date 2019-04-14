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
    sold = db.Column(db.Integer())
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'), default=1)
    category = db.relationship('Category', lazy=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    average_rating = db.Column(db.Float, default=0.0, nullable=True)
    ratings = db.relationship('ProductRating', lazy=True)

    def __str__(self):
        return self.name
