from .base_model import BaseModel, db

class OrderDetail(BaseModel):
	__tablename__ = 'order_details'

	item_id = db.Column(db.Integer(), primary_key=True)
	order_id = db.Column(db.Integer(), db.ForeignKey('orders.order_id'), nullable=False, default=1)
	order = db.relationship('Order', lazy=False)
	product_id = db.Column(db.Integer(), nullable=False)
	attributes = db.Column(db.String(1000), nullable=False)
	product_name = db.Column(db.String(100), nullable=False)
	quantity = db.Column(db.Integer())
	unit_cost = db.Column(db.DECIMAL())
