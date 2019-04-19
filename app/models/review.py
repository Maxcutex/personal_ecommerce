from .base_model import BaseModel, db

class Review(BaseModel):
	__tablename__ = 'review'

	review_id = db.Column(db.Integer(), primary_key=True)
	customer_id = db.Column(db.Integer(), db.ForeignKey('customers.customer_id'), default=1)
	customer = db.relationship('Customer', lazy=False)
	product_id = db.Column(db.Integer(), db.ForeignKey('products.product_id'), default=1)
	product = db.relationship('Product', lazy=False)
	review = db.Column(db.Text(), nullable=False)
	rating = db.Column(db.SmallInteger())
	created_on = db.Column(db.DateTime(), nullable=False)
