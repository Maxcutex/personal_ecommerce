'''Module for ProductRating Model class'''
from .base_model import BaseModel, db


class ProductRating(BaseModel):
	__tablename__='product_ratings'

	product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
	user_id = db.Column(db.String(100))
	comment = db.Column(db.String(1000), nullable=True)
	rating = db.Column(db.Float())
	channel = db.Column(db.String(100))
	Product = db.relationship('Product', lazy=False)