from .base_model import BaseModel, db


class UserRole(BaseModel):
	__tablename__ = 'user_roles'

	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('users.customer_id'), default=1, primary_key=True)
	user = db.relationship('User', lazy=False)
	is_active = db.Column(db.Boolean, default=True, nullable=True)
