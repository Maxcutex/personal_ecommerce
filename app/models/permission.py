from .base_model import BaseModel, db


class Permission(BaseModel):
	__tablename__ = 'permission'

	id = db.Column(db.Integer(), primary_key=True)
	role_id = db.Column(db.Integer(), db.ForeignKey('role.role_id'))
	name = db.Column(db.String(100), nullable=False)
	keyword = db.Column(db.String(100), nullable=False)

	def __str__(self):
		return '<Permission: {}>'.format(self.name)
