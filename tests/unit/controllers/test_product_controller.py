'''Unit tests for the product controller.
'''
from datetime import datetime
from unittest.mock import patch, Mock
from faker import Faker

from app.controllers.product_controller import ProductController
from app.models.product import Product
from app.models.product_rating import ProductRating
from tests.base_test_case import BaseTestCase


class TestProductController(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()
		self.fake = Faker()

		self.mock_rating = ProductRating(
			product_rating_id=1,
			created_at=datetime.now(),
			updated_at=datetime.now(),
			product_id=1,
			user_id=1,
			rating=1.2,
			channel='web'
		)
		self.mock_product_with_dependants = Product(
			product_id=1,
			created_at=datetime.now(),
			updated_at=datetime.now(),
			is_deleted=False,
			name=self.fake.name(),
			description=self.fake.name(),
			price=34.5,
			discounted_price=23.5,
			display=20,
			sold=10,
			is_active=True,
			ratings=[self.mock_rating, ],
		)
		self.mock_product = Product(
			product_id=1,
			created_at=datetime.now(),
			updated_at=datetime.now(),
			is_deleted=False,
			name=self.fake.name(),
			description=self.fake.name(),
			price=34.5,
			discounted_price=23.5,
			display=20,
			sold=10,
			is_active=True
		)
		self.mock_deleted_product = Product(
			product_id=1,
			created_at=datetime.now(),
			updated_at=datetime.now(),
			is_deleted=True,
			name=self.fake.name(),
			description=self.fake.name(),
			price=34.5,
			discounted_price=23.5,
			display=20,
			sold=10,
			is_active=True
		)

	@patch('app.repositories.product_repo.ProductRepo.filter_by')
	@patch('app.controllers.product_controller.ProductController'
		   '.pagination_meta')
	def test_list_products_ok_response(
			self,
			mock_pagination_meta,
			mock_filter_by
	):
		'''Test list_products OK response.
        '''
		# Arrange
		with self.app.app_context():
			mock_pagination_meta.return_value = {
				'total_rows': 1,
				'total_pages': 1,
				'current_page': 1,
				'next_page': 1,
				'prev_page': 1
			}
			mock_filter_by.return_value.items = [
				self.mock_product,
			]
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.list_products()

			# Assert
			assert result.status_code == 200
			assert result.get_json()['msg'] == 'OK'

	# noinspection PyUnresolvedReferences
	@patch('app.utils.auth.Auth.get_location')
	@patch('app.repositories.product_repo.ProductRepo.filter_by')
	@patch.object(ProductController, 'pagination_meta')
	def test_list_deleted_products_ok_response(
			self,
			mock_pagination_meta,
			mock_filter_by,
			mock_get_location
	):
		'''Test list_deleted_products OK response.
        '''
		# Arrange
		with self.app.app_context():
			mock_pagination_meta.return_value = {
				'total_rows': 1,
				'total_pages': 1,
				'current_page': 1,
				'next_page': 1,
				'prev_page': 1
			}
			mock_filter_by.return_value.items = [self.mock_product, ]
			mock_get_location.return_value = 1
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.list_deleted_products()

			# Assert
			assert result.status_code == 200
			assert result.get_json()['msg'] == 'OK'

	@patch('app.repositories.product_repo.ProductRepo.filter_by')
	@patch.object(ProductController, 'pagination_meta')
	def test_list_suspended_products_ok_response(
			self,
			mock_pagination_meta,
			mock_filter_by
	):
		'''Test list_deleted_products OK response.
        '''
		# Arrange
		with self.app.app_context():
			mock_pagination_meta.return_value = {
				'total_rows': 1,
				'total_pages': 1,
				'current_page': 1,
				'next_page': 1,
				'prev_page': 1
			}
			mock_filter_by.return_value.items = [self.mock_product, ]
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.list_suspended_products()

			# Assert
			assert result.status_code == 200
			assert result.get_json()['msg'] == 'OK'

	@patch('app.repositories.product_repo.ProductRepo.get')
	def test_get_product_when_product_doesnot_exist(
			self,
			mock_product_repo_get
	):
		'''Test get_product when the product doesnot exist.
        '''
		# Arrange
		with self.app.app_context():
			mock_product_repo_get.return_value = None
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.get_product(1)

			# Assert
			assert result.status_code == 400
			assert result.get_json()['msg'] == 'Bad Request - Invalid or ' \
											   'Missing product_id'
	def test_product_search_with_response(self):
		pass

	def test_product_get_product_invalid_response(self):
		pass

	def test_product_get_product_in_category(self):
		pass

	def test_product_get_product_in_department(self):
		pass

	def test_get_product_details(self):
		pass

	def test_get_product_location(self):
		pass

	def test_get_product_reviews(self):
		pass

	def test_post_product_reviews(self):
		pass

	@patch('app.repositories.product_repo.ProductRepo.get')
	def test_get_product_ok_response(
			self,
			mock_product_repo_get
	):
		'''Test get_product OK response.
        '''
		# Arrange
		with self.app.app_context():
			mock_product_repo_get.return_value = self.mock_product
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.get_product(1)

			# Assert
			assert result.status_code == 200
			assert result.get_json()['msg'] == 'OK'

	@patch.object(ProductController, 'request_params')
	@patch('app.repositories.product_repo.ProductRepo.new_product')
	def test_creat_product_ok_response(
			self,
			mock_new_product,
			mock_request_params
	):
		'''Test create_product OK response.
        '''
		mock_request_params.return_value = (
			self.fake.name(), self.fake.text(),
			self.fake.pydecimal(left_digits=2, right_digits=2, positive=True),
			self.fake.pydecimal(left_digits=2, right_digits=2, positive=True),
			self.fake.name(), self.fake.name(), self.fake.name(),
			20, 3, 1, [2,3]
		)
		mock_new_product.return_value = self.mock_product
		product_controller = ProductController(self.request_context)

		# Act
		result = product_controller.create_product()

		# Assert
		assert result.status_code == 201
		assert result.get_json()['msg'] == 'OK'

	@patch.object(ProductController, 'request_params')
	@patch('app.repositories.product_repo.ProductRepo.get')
	def test_update_product_when_product_doesnot_exist(
			self,
			mock_product_repo_get,
			mock_request_params
	):
		'''Test update_product when product does not exist.
        '''
		# Arrange
		with self.app.app_context():
			mock_request_params.return_value = (
				self.fake.name(), self.fake.text(),
				self.fake.pydecimal(left_digits=2, right_digits=2, positive=True),
				self.fake.pydecimal(left_digits=2, right_digits=2, positive=True),
				self.fake.name(), self.fake.name(), self.fake.name(),
				20, 3, 1
			)
			mock_product_repo_get.return_value = None
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.update_product(1)

			# Assert
			assert result.status_code == 400
			assert result.get_json()['msg'] == 'Invalid or incorrect ' \
											   'product_id provided'

	@patch.object(ProductController, 'request_params')
	@patch('app.repositories.product_repo.ProductRepo.get')
	def test_update_product_ok_response(
			self,
			mock_product_repo_get,
			mock_request_params
	):
		'''Test update_product OK response.
        '''
		# Arrange
		with self.app.app_context():
			mock_request_params.return_value = (
				self.fake.name(), self.fake.text(),
				self.fake.pydecimal(left_digits=2, right_digits=2, positive=True),
				self.fake.pydecimal(left_digits=2, right_digits=2, positive=True),
				self.fake.name(), self.fake.name(), self.fake.name(),
				20, 3, 1
			)
			mock_product_repo_get.return_value = self.mock_product
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.update_product(1)

			# Assert
			assert result.status_code == 200
			assert result.get_json()['msg'] == 'OK'

	@patch('app.repositories.product_repo.ProductRepo.get')
	def test_suspend_product_when_product_doesnot_exist(
			self,
			mock_product_repo_get
	):
		'''Test suspend_product when product doesnot exist.
        '''
		# Arrange
		with self.app.app_context():
			mock_product_repo_get.return_value = None
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.suspend_product(1)

			# Assert
			assert result.status_code == 400
			assert result.get_json()['msg'] == 'Invalid or incorrect ' \
											   'product_id provided'

	@patch('app.repositories.product_repo.ProductRepo.get')
	@patch('app.repositories.product_repo.ProductRepo.update')
	def test_suspend_product_ok_response(
			self,
			mock_product_repo_update,
			mock_product_repo_get
	):
		'''Test suspend_product OK response.
        '''
		# Arrange
		with self.app.app_context():
			mock_product_repo_get.return_value = self.mock_product
			mock_product_repo_update.return_value = self.mock_product
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.suspend_product(1)

			# Assert
			assert result.status_code == 200
			assert result.get_json()['msg'] == 'OK'

	@patch('app.repositories.product_repo.ProductRepo.get')
	def test_un_suspend_product_when_product_doesnot_exist(
			self,
			mock_product_repo_get
	):
		'''Test un_suspend_product when product doesnot exist.
        '''
		# Arrange
		with self.app.app_context():
			mock_product_repo_get.return_value = None
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.un_suspend_product(1)

			# Assert
			assert result.status_code == 400
			assert result.get_json()['msg'] == 'Invalid or incorrect ' \
											   'product_id provided'

	@patch('app.repositories.product_repo.ProductRepo.get')
	@patch('app.repositories.product_repo.ProductRepo.update')
	def test_un_suspend_product_ok_response(
			self,
			mock_product_repo_update,
			mock_product_repo_get
	):
		'''Test un_suspend_product OK response.
        '''
		# Arrange
		with self.app.app_context():
			mock_product_repo_get.return_value = self.mock_product
			mock_product_repo_update.return_value = self.mock_product
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.un_suspend_product(1)

			# Assert
			assert result.status_code == 200
			assert result.get_json()['msg'] == 'OK'

	@patch('app.repositories.product_repo.ProductRepo.get')
	def test_delete_product_when_product_doesnot_exist(
			self,
			mock_product_repo_get
	):
		'''Test delete_product when product doesnot exist.
        '''
		# Arrange
		with self.app.app_context():
			mock_product_repo_get.return_value = None
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.delete_product(1)

			# Assert
			assert result.status_code == 400
			assert result.get_json()['msg'] == 'Invalid or incorrect ' \
											   'product_id provided'

	@patch('app.repositories.product_repo.ProductRepo.get')
	def test_delete_product_when_product_is_already_deleted(
			self,
			mock_product_repo_get
	):
		'''Test delete_product when product is already deleted.
        '''
		# Arrange
		with self.app.app_context():
			mock_product_repo_get.return_value = self.mock_deleted_product
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.delete_product(1)

			# Assert
			assert result.status_code == 400
			assert result.get_json()['msg'] == 'product has already ' \
											   'been deleted'

	# @patch('app.repositories.product_repo.ProductRepo.get')
	# def test_delete_product_when_product_has_dependants(
	# 		self,
	# 		mock_product_repo_get
	# ):
	# 	'''Test delete_product when product has dependants.
     #    '''
	# 	# Arrange
	# 	with self.app.app_context():
	# 		mock_product_repo_get.return_value = \
	# 			self.mock_product_with_dependants
	# 		product_controller = ProductController(self.request_context)
	#
	# 		# Act
	# 		result = product_controller.delete_product(1)
	#
	# 		# Assert
	# 		assert result.status_code == 400
	# 		assert result.get_json()['msg'] == 'product cannot be deleted ' \
	# 										   'because it has a child object'

	@patch('app.repositories.product_repo.ProductRepo.get')
	@patch('app.repositories.product_repo.ProductRepo.update')
	def test_delete_product_ok_response(
			self,
			mock_product_repo_update,
			mock_product_repo_get
	):
		'''Test delete_product OK response.
        '''
		# Arrange
		with self.app.app_context():
			mock_product_repo_get.return_value = self.mock_product
			mock_product_repo_update.return_value = self.mock_product
			product_controller = ProductController(self.request_context)

			# Act
			result = product_controller.delete_product(1)

			# Assert
			assert result.status_code == 200
			assert result.get_json()['msg'] == 'product deleted'
