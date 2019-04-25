from .base_model import BaseModel, db

class Order(BaseModel):
	__tablename__ = 'order'

	order_id = db.Column(db.Integer(), primary_key=True)
	total_amount = db.Column(db.DECIMAL(), nullable=False)
	created_on = db.Column(db.DateTime(), nullable=False)
	shipped_on = db.Column(db.DateTime())
	status = db.Column(db.Integer(), nullable=False, default=0)
	comments = db.Column(db.String(255))
	auth_code = db.Column(db.String(50))
	reference = db.Column(db.String(50))
	customer_id = db.Column(db.Integer(), db.ForeignKey('customer.customer_id'), default=1)
	customer = db.relationship('Customer', lazy=False)
	shipping_id = db.Column(db.Integer(), db.ForeignKey('shipping.shipping_id'), default=1)
	shipping = db.relationship('Shipping', lazy=False)
	tax_id = db.Column(db.Integer(), db.ForeignKey('tax.tax_id'), default=1)
	tax = db.relationship('Tax', lazy=False)
