"""module of User model class"""
from .base_model import BaseModel, db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta

class User(BaseModel):
	"""User Model class"""
	__tablename__ = 'users'

	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	email = db.Column(db.String(100))
	address_1 = db.Column(db.String(100), nullable=True)
	address_2 = db.Column(db.String(100), nullable=True)
	city = db.Column(db.String(100), nullable=True)
	region = db.Column(db.String(100), nullable=True)
	postal_code = db.Column(db.String(100), nullable=True)
	country = db.Column(db.String(100), nullable=True)
	shipping_region_id = db.Column(db.String(100), nullable=True)
	day_phone = db.Column(db.String(100), nullable=True)
	eve_phone = db.Column(db.String(100), nullable=True)
	mob_phone = db.Column(db.String(100), nullable=True)
	password_hash = db.Column(db.String(128))
	department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
	is_admin = db.Column(db.Boolean, default=False)

	department = db.relationship('Department', lazy=False)

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
		self.password_hash = Bcrypt().generate_password_hash(password)

	def verify_password(self, password):
		"""
		Check if hashed password matches actual password
		"""
		return Bcrypt().check_password_hash(self.password_hash, password)

	def generate_token(self, user_id):
		"""Generates the access token to be used as the Authorization header"""

		try:
			# set up a payload with an expiration time
			payload = {
				'exp': datetime.utcnow() + timedelta(minutes=5),
				'iat': datetime.utcnow(),
				'sub': user_id
			}
			# create the byte string token using the payload and the SECRET key
			jwt_string = jwt.encode(
				payload,
				"SECRET_KEY", #current_app.config.get('SECRET'),
				algorithm='HS256'
			)
			return jwt_string

		except Exception as e:
			# return an error in string format if an exception occurs
			return str(e)
