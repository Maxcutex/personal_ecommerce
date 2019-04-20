from datetime import datetime

from app.controllers.base_controller import BaseController
from app.repositories.product_repo import ProductRepo
from app.repositories.shopping_cart_repo import ShoppingCartRepo


class ShoppingCartController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.shopping_cart_repo = ShoppingCartRepo()
		self.product_repo = ProductRepo()

	def generate_unique_id(self):
		pass

	def get_shopping_cart_by_id(self, cart_id):
		shopping_cart_list = self.product_repo.filter_by(cart_id=cart_id)
		shopping_array = []
		if shopping_cart_list:
			for cart in shopping_cart_list:

				shopping_cart = []
				sub_total_price = cart.quantity * cart.product.price
				shopping_cart['name'] = cart.product.name
				shopping_cart['price'] = cart.product.price
				shopping_cart['subtotal'] = sub_total_price
				shopping_cart['quantity'] = cart.quantity
				shopping_cart['item_id'] = cart.item_id
				shopping_cart['attributes'] = cart.attributes
				shopping_array.append(shopping_cart)
			return self.handle_response('OK', payload={shopping_array})
		else:
			return self.handle_response('Bad Request - Invalid or Missing cart_id', status_code=400)

	def get_saved_cart_by_id(self, cart_id):
		shopping_cart_list = self.product_repo.filter_by(cart_id=cart_id, buy_now=False)
		shopping_array = []
		if shopping_cart_list:
			for cart in shopping_cart_list:

				shopping_cart = []
				shopping_cart['name'] = cart.product.name
				shopping_cart['price'] = cart.product.price
				shopping_cart['item_id'] = cart.item_id
				shopping_cart['attributes'] = cart.attributes
				shopping_array.append(shopping_cart)
			return self.handle_response('OK', payload={shopping_array})
		else:
			return self.handle_response('Bad Request - Invalid or Missing cart_id', status_code=400)

	def create_cart(self):
		cart_id, product_id, attributes = self.request_params(
			'cart_id', 'product_id', 'attributes'
		)
		quantity = 1
		buy_now = False
		added_on = datetime.now()

		# check if item was previously added with cart_id
		cart_item_exists = self.shopping_cart_repo.find_first(cart_id=cart_id, product_id=product_id)
		if cart_item_exists:
			updates = {}
			new_quantity = cart_item_exists.quantity + 1
			updates['quantity'] = new_quantity
			quantity = new_quantity
			cart = self.shopping_cart_repo.update(cart_item_exists, **updates)
		else:
			cart = self.shopping_cart_repo.new_cart(cart_id, product_id, attributes, quantity, buy_now,
													added_on)
		sub_total_price = quantity * cart.product.price

		cart['name'] = cart.product.name
		cart['price'] = cart.product.price
		cart['subtotal'] = sub_total_price

		return self.handle_response('OK', payload={cart.serialize()}, status_code=201)

	def get_total_amount(self, cart_id):
		shopping_cart_list = self.shopping_cart_repo.filter_by(cart_id=cart_id)
		total_amount = 0
		total_amount_display = {}
		for shopping_cart in shopping_cart_list:
			sub_total_price = shopping_cart.quantity * shopping_cart.product.price
			total_amount = total_amount + sub_total_price

		total_amount_display['total_amount'] = total_amount
		return self.handle_response('OK', payload={total_amount_display})

	def save_for_later(self, item_id):
		shopping_cart = self.shopping_cart_repo.get(item_id)
		if shopping_cart:
			updates = {}
			updates['buy_now'] = False

			self.shopping_cart_repo.update(shopping_cart, **updates).serialize()
			return self.handle_response('OK', payload={})


	def update_shopping_cart(self, item_id):
		item_id, quantity = self.request_params('item_id', 'quantity')
		shopping_cart = self.shopping_cart_repo.get(item_id)
		if shopping_cart:
			updates = {}
			updates['item_id'] = item_id
			updates['quantity'] = quantity

			cart = self.shopping_cart_repo.update(shopping_cart, **updates).serialize()
			sub_total_price = quantity * shopping_cart.product.price
			cart['subtotal'] = sub_total_price
			return self.handle_response('OK', payload={cart})

		return self.handle_response('Invalid or incorrect cart_id provided', status_code=400)

	def delete_shopping_cart(self, cart_id):
		shopping_cart_list = self.shopping_cart_repo.filter_by(cart_id=cart_id)
		if shopping_cart_list:
			self.shopping_cart_repo.delete_item(cart_id=cart_id)

			return self.handle_response('Ok', payload={[]})
		return self.handle_response('Invalid or incorrect cart_id provided', status_code=400)

	def delete_cart_item(self, item_id):
		shopping_cart = self.shopping_cart_repo.filter_by(item_id=item_id)
		if shopping_cart:
			self.shopping_cart_repo.delete_item(item_id=item_id)

			return self.handle_response('Ok', payload={[]})
		return self.handle_response('Invalid or incorrect cart_id provided', status_code=400)

