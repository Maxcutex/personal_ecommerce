from .base_model import BaseModel, db

class Audit(BaseModel):
	__tablename__ = 'audit'

	audit_id = db.Column(db.Integer(), primary_key=True)
	order_id = db.Column(db.Integer(), db.ForeignKey('order.order_id'), nullable=False, default=1)
	order = db.relationship('Order', lazy=False)
	created_on = db.Column(db.DateTime(), nullable=False)
	message = db.Column(db.Text(), nullable=False)
	code = db.Column(db.Integer())
