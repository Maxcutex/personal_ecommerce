'''Module for ProductRating Model class'''
from .base_model import BaseModel, db


class ProductRating(BaseModel):
	__tablename__='product_ratings'

	product_rating_id = db.Column(db.Integer(), primary_key=True)
	product_id = db.Column(db.Integer(), db.ForeignKey('products.product_id'))
	user_id = db.Column(db.String(100))
	comment = db.Column(db.String(1000), nullable=True)
	rating = db.Column(db.Float())
	channel = db.Column(db.String(100))
	Product = db.relationship('Product', lazy=False)
