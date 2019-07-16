from flask import Blueprint, request
from app.utils.security import Security
from app.utils.auth import Auth


class BaseBlueprint:
	
	base_url_prefix = '/api/v1'
	
	def __init__(self, app):
		self.app = app
	
	def register(self):
		
		''' Register All App Blue Prints Here '''
		
		from app.blueprints import (
			home_blueprint, attribute_blueprint, customer_blueprint, department_blueprint, category_blueprint
		)

		self.app.register_blueprint(attribute_blueprint)
		self.app.register_blueprint(home_blueprint)
		self.app.register_blueprint(customer_blueprint)
		self.app.register_blueprint(department_blueprint)
		self.app.register_blueprint(category_blueprint)