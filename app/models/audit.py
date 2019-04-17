from .base_model import BaseModel, db

class Audit(BaseModel):
	__tablename__ = 'audit'

	order_id = db.Column(db.Integer(), db.ForeignKey('orders.id'), nullable=False, default=1)
	order = db.relationship('Order', lazy=False)
	created_on = db.Column(db.DateTime(), nullable=False)
	message = db.Column(db.Text(), nullable=False)
	code = db.Column(db.Integer())
