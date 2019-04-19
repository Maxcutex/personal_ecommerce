"""module of attribute model class"""
from .base_model import BaseModel, db
from flask_bcrypt import Bcrypt


class Customer(BaseModel):
	"""Customer Model class"""
	__tablename__ = 'customers'

	name = db.Column(db.String(100))
	email = db.Column(db.String(100))
	address_1 = db.Column(db.String(100))
	address_1 = db.Column(db.String(100))
	city = db.Column(db.String(100))
	region = db.Column(db.String(100))
	postal_code = db.Column(db.String(100))
	country = db.Column(db.String(100))
	shipping_region_id = db.Column(db.String(100))
	day_phone = db.Column(db.String(100))
	eve_phone = db.Column(db.String(100))
	mob_phone = db.Column(db.String(100))
	password_hash = db.Column(db.String(128))
	department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	is_admin = db.Column(db.Boolean, default=False)

	def password_is_valid(self, password):
		"""
		Checks the password against it's hash to validates the user's password
		"""
		return Bcrypt().check_password_hash(self.password, password)

	@property
	def password(self):
		"""
		Prevent pasword from being accessed
		"""
		raise AttributeError('password is not a readable attribute.')

	@password.setter
	def password(self, password):
		"""
		Set password to a hashed password
		"""
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		"""
		Check if hashed password matches actual password
		"""
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
	return Employee.query.get(int(user_id))

	def __str__(self):
		return self.name