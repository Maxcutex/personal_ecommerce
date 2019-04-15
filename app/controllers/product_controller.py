'''A controller module for product-related
'''
from app.controllers.base_controller import BaseController
from app.repositories.product_repo import ProductRepo
from app.repositories.product_rating_repo import ProductRatingRepo
from app.utils.auth import Auth


class ProductController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.product_repo = ProductRepo()
		self.product_rating_repo = ProductRatingRepo()

	def list_products(self):
		products = self.product_repo.filter_by_asc(
			self.product_repo._model.name,
			is_deleted=False,
			is_active=True)
		products_list = [product.serialize() for product in products.items]
		return self.handle_response('OK', payload={'products': products_list, 'meta': self.pagination_meta(products)})

	def list_deleted_products(self):
		products = self.product_repo.filter_by(is_deleted=True)
		products_list = [product.serialize() for product in products.items]
		return self.handle_response('OK', payload={'products': products_list, 'meta': self.pagination_meta(products)})

	def list_suspended_products(self):
		products = self.product_repo.filter_by(is_deleted=False, is_active=False)
		products_list = [product.serialize() for product in products.items]
		return self.handle_response('OK', payload={'products': products_list, 'meta': self.pagination_meta(products)})

	def get_product(self, product_id):
		product = self.product_repo.get(product_id)
		if product:
			product = product.serialize()
			return self.handle_response('OK', payload={'product': product})
		else:
			return self.handle_response('Bad Request - Invalid or Missing product_id', status_code=400)

	def create_product(self):
		name,  description, price, discounted_price, image, image2, thumbnail, display, sold, category_id = self.request_params(
			'name', 'description', 'price', 'discounted_price', 'image', 'image2', 'thumbnail', 'display', 'sold', 'category_id')

		product = self.product_repo.new_product(
			name, description, price, discounted_price, image, image2, thumbnail, display, sold, category_id
		).serialize()
		return self.handle_response('OK', payload={'product': product}, status_code=201)

	def update_product(self, product_id):
		name, description, price, discounted_price, image, image2, thumbnail, display, sold, category_id = self.request_params(
			'name', 'description', 'price', 'discounted_price', 'image', 'image2', 'thumbnail', 'display', 'sold',
			'category_id')
		product = self.product_repo.get(product_id)
		if product:
			updates = {}
			if name:
				updates['name'] = name
			if description:
				updates['description'] = description
			if price:
				updates['price'] = price
			if discounted_price:
				updates['discounted_price'] = discounted_price
			if image:
				updates['image'] = image
			if image2:
				updates['image2'] = image2
			if thumbnail:
				updates['thumbnail'] = thumbnail
			if display:
				updates['display'] = display
			if image:
				updates['sold'] = sold

			self.product_repo.update(product, **updates)
			return self.handle_response('OK', payload={'product': product.serialize()})

		return self.handle_response('Invalid or incorrect product_id provided', status_code=400)

	def suspend_product(self, product_id):
		product = self.product_repo.get(product_id)
		if product:
			updates = {}
			updates['is_active'] = 0
			self.product_repo.update(product, **updates)
			return self.handle_response('OK', payload={'product': product.serialize()})
		return self.handle_response('Invalid or incorrect product_id provided', status_code=400)

	def un_suspend_product(self, product_id):
		product = self.product_repo.get(product_id)
		if product:
			updates = {}
			updates['is_active'] = 1
			self.product_repo.update(product, **updates)
			return self.handle_response('OK', payload={'product': product.serialize()})
		return self.handle_response('Invalid or incorrect product_id provided', status_code=400)

	def delete_product(self, product_id):
		product = self.product_repo.get(product_id)
		if product:
			if product.is_deleted:
				return self.handle_response('product has already been deleted', status_code=400)

			#if any(not dependent.is_deleted for dependent in (product.engagements or product.ratings)):
			#	return self.handle_response('product cannot be deleted because it has a child object', status_code=400)
			updates = {}
			updates['is_deleted'] = True

			self.product_repo.update(product, **updates)


			return self.handle_response('product deleted', payload={"status": "success"})
		return self.handle_response('Invalid or incorrect product_id provided', status_code=400)
