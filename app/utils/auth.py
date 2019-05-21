from functools import wraps
from datetime import datetime, timedelta
from flask import request, jsonify, make_response
from os import getenv
from base64 import b64decode
from app.utils.security import Security
from app.repositories import RoleRepo, UserRoleRepo, PermissionRepo
import ast

import jwt

class Auth:
	''' This class will house Authentication and Authorization Methods '''
	
	''' Routes The Location Header Should Not Be Applied To'''
	location_header_ignore = [
		'/locations'
	]
	
	''' Routes The Authentication Header Should Not Be Applied To'''
	authentication_header_ignore = [
		# to ignore specific methods on a path use 'path:method1:method2:method3 etc...
		'/docs', 'customers/:post',
	]

	@staticmethod
	def generate_token(user_info, exp=24):
		"""
		Generates jwt tokens for testing purpose

		params:
			exp: Token Expiration. This could be datetime object or an integer
		result:
			token: This is the bearer token in this format 'Bearer token'
		"""

		decode_secret_key = lambda key_64: b64decode(key_64).decode('utf-8')

		secret_key = decode_secret_key(getenv('JWT_SECRET_KEY'))

		issue_date = datetime.now()

		payload = {
			'UserInfo': user_info,
			'iat': issue_date,
			'exp': issue_date + timedelta(hours=exp)
		}

		token = jwt.encode(payload, secret_key, algorithm='RS256').decode('utf-8')
		return f'Bearer {token}'
	
	@staticmethod
	def check_token():
		if request.method != 'OPTIONS':

			# if '/' in Auth.authentication_header_ignore:
			# 	return None

			for endpoint in Auth.authentication_header_ignore:
				endpoint, *methods = endpoint.split(':')

				if_condition = (
						request.path.find(endpoint) > -1) if not methods else (
						request.path.find(endpoint) > -1 and request.method.lower() in
						map(lambda key: key.lower(), methods)
				)

				if if_condition: # If endpoint in request.path, ignore this check
					return None

			try:
				token = Auth.get_token()
			except Exception as e:
				error_msg = ast.literal_eval(str(e))
				return make_response(jsonify({'error': error_msg}),400)

			try:
				decoded = Auth.decode_token(token)
			except Exception as e:
				return make_response(jsonify({'msg': str(e)}), 400)

	@staticmethod
	def _get_user():
		token = None
		try:
			token = Auth.get_token()
		except Exception as e:
			raise e
		
		try:
			if token:
				return Auth.decode_token(token)['UserInfo']
		except Exception as e:
			raise e
	
	@staticmethod
	def user(*keys):
		user = Auth._get_user()
		if keys:
			if len(keys) > 1:
				values = list()
				for key in keys:
					values.append(user[key]) if key in user else values.append(None)
				return values
			if len(keys) == 1 and keys[0] in user:
				return user[keys[0]]
		
		return user
	
	@staticmethod
	def get_token(request_obj=None):
		if request_obj:
			header = request_obj.headers.get('USER-KEY', None)
		else:
			header = request.headers.get('USER-KEY', None)
		if not header:
			error_msg = Security.error_msg('AUT_01', 'USER-KEY', 'Authorization code is empty.', 'header')
			raise Exception(error_msg)
		
		header_parts = header.split()
		
		if header_parts[0].lower() != 'bearer':
			error_msg = Security.error_msg('AUT_01', 'USER-KEY', 'Authorization Header Must Start With "Bearer "',
										   'header')
			raise Exception(error_msg)
		elif len(header_parts) > 1:
			return header_parts[1]
		
		raise Exception('Internal Application Error')
	
	@staticmethod
	def decode_token(token):

		public_key = Auth._get_jwt_public_key()

		try:
			decoded = jwt.decode(
				token,
				public_key,
				algorithms=['RS256'],
				options={
					'verify_signature': True,
					'verify_exp': True
				})
			return decoded
		except jwt.ExpiredSignature:
			raise Exception('Token is Expired')
		except jwt.DecodeError:
			raise Exception('Error Decoding')

	@staticmethod
	def _get_jwt_public_key():
		decode_public_key = lambda key_64: b64decode(key_64).decode('utf-8')

		jwt_env_mapper = {
			'testing': 'JWT_PUBLIC_KEY_TEST',
			'production': 'JWT_PUBLIC_KEY',
			'development': 'JWT_PUBLIC_KEY',
			'staging': 'JWT_PUBLIC_KEY'
		}

		public_key_mapper = {
			'testing': lambda key: key,
			'development': decode_public_key,
			'production': decode_public_key,
			'staging': decode_public_key,
		}

		app_env = getenv('APP_ENV', 'production')

		public_key_64 = getenv(jwt_env_mapper.get(app_env, 'JWT_PUBLIC_KEY'))

		public_key = public_key_mapper.get(app_env, decode_public_key)(public_key_64)

		return public_key
		
	@staticmethod
	def check_location_header():
		if request.method != 'OPTIONS':
			for endpoint in Auth.location_header_ignore:
				if request.path.find(endpoint) > -1: # If endpoint in request.path, ignore this check
					return None
			try:
				Auth.get_location()
			except Exception as e:
				return make_response(jsonify({'msg': str(e)}), 400)
		
	@staticmethod
	def get_location():
		location = request.headers.get('X-Location', None)
		if not location:
			raise Exception('Location Header is Expected')
		if not location.isdigit():
			raise Exception('Location Header Value is Invalid')
		return int(location)
	
	@staticmethod
	def has_permission(permission):
		
		def permission_checker(f):
			
			@wraps(f)
			def decorated(*args, **kwargs):
				user_role_repo = UserRoleRepo()
				permission_repo = PermissionRepo()
				
				user_id = Auth.user('id')
				user_role = user_role_repo.find_first(**{'user_id': user_id})
				
				if not user_id:
					return make_response(jsonify({'msg': 'Missing User ID in token'})), 400

				if not user_role:
					return make_response(jsonify({'msg': 'Access Error - No Role Granted'})), 400

				user_perms = permission_repo.filter_by(**{'role_id': user_role.role_id})
				
				perms = [perm.keyword for perm in user_perms.items]
				if len(perms) == 0:
						return make_response(jsonify({'msg': 'Access Error - No Permission Granted'})), 400
				
				if permission not in perms:
					return make_response(jsonify({'msg': 'Access Error - Permission Denied'})), 400
				
				return f(*args, **kwargs)
			
			return decorated
		return permission_checker


	@staticmethod
	def has_role(role):

		def role_checker(f):

			@wraps(f)
			def decorated(*args, **kwargs):

				user_role_repo = UserRoleRepo()

				role_repo = RoleRepo()

				user = Auth.user('id')
				user_id = user.get('customerId') if user else None

				user_role = user_role_repo.find_first(**{'user_id': user_id})

				if not user_id:
					return make_response(jsonify({'msg': 'Missing User ID in token'})), 400

				if not user_role:
					return make_response(jsonify({'msg': 'Access Error - No Role Granted'})), 400

				if role_repo.get(user_role.role_id).name != role:
					return make_response(
						jsonify({'msg': 'Access Error - This role does not have the access rights'}
								)
					), 400

				return f(*args, **kwargs)

			return decorated

		return role_checker
	
		