from datetime import datetime

from app.controllers.base_controller import BaseController
from app.repositories import CustomerRepo
from app.repositories.order_detail_repo import OrderDetailRepo
from app.repositories.order_repo import OrderRepo
from app.repositories.shopping_cart_repo import ShoppingCartRepo


class OrderController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.order_repo = OrderRepo()
		self.order_detail_repo = OrderDetailRepo()
		self.shopping_cart_repo = ShoppingCartRepo()
		self.customer_repo = CustomerRepo()

	def get_orders_by_order_id(self, order_id):
		order_details = self.order_detail_repo.filter_by(order_id=order_id)
		order_list = {}
		if order_details:
			for order_detail in order_details:
				order_object = {'order_id': order_detail.order_id, 'product_id': order_detail.product_id,
								'attributes': order_detail.attributes, 'product_name': order_detail.product_name,
								'quantity': order_detail.quantity, 'unit_cost': order_detail.unit_cost,
								'subtotal': order_detail.quantity * order_detail.unit_cost}
				order_list.append(order_object)

			return self.handle_response('OK', payload={order_list})

		else:
			return self.handle_response('Bad Request. This order details for this order id could not be found', status_code=400)

	def get_orders_short_detail_by_order_id(self, order_id):
		order = self.order_repo.filter_by(order_id=order_id)

		if order:
			customer = self.customer_repo.get(order.customer_id)
			order_dict = {
				'order_id': order.order_id, 'total_amount': order.total_amount,
				'created_on': order.created_on, 'shipped_on': order.shipped_on, 'status': order.status,
				'name': customer.name
			}

			return self.handle_response('OK', payload={order_dict})

		else:
			return self.handle_response('Bad Request. This categories for this product does not exist', status_code=400)

	def get_orders_by_customer(self, department_id):
		department_categories = self.order_repo.filter_by(department_id=department_id)
		department_category_array = []

		if department_categories:
			for category_id in department_categories:
				category = self.category_repo.get(category_id)
				category_object = []
				category_object['name'] = category.name
				category_object['department_id'] = category.department_id
				category_object['description'] = category.description
				department_category_array.append(category_object)

			return self.handle_response('OK', payload={department_category_array})

		else:
			return self.handle_response('Bad Request. This categories for this department does not exist',
										status_code=400)

	def create_order(self):

		cart_id, shipping_id, tax_id = self.request_params_dict(
			'cart_id', 'shipping_id', 'tax_id')

		shopping_cart_list = self.shopping_cart_repo.filter_by(cart_id=cart_id, buy_now=True)
		total_amount = 0
		for shopping_cart in shopping_cart_list:
			sub_total_price = shopping_cart.quantity * shopping_cart.product.price
			total_amount = total_amount + sub_total_price
		created_on = datetime.now()
		customer_id = 0 # get from session
		shipping_id = shipping_id
		tax_id = tax_id
		order = self.order_repo.new_order(
			total_amount=total_amount, created_on=created_on, customer_id=customer_id,
			shipping_id=shipping_id, tax_id=tax_id
		)

		for shopping_cart in shopping_cart_list:
			unit_cost = shopping_cart.product.price

			self.order_detail_repo.new_order_detail(
				order_id=order.id, product_id=shopping_cart.product_id, attributes=shopping_cart.attributes,
				product_name=shopping_cart.product.name, quantity=shopping_cart.quantity, unit_cost=unit_cost
			)

		serialized_order_data = order.serialize()
		if order:
			self.shopping_cart_repo.delete(cart_id=cart_id, buy_now=True)

		return self.handle_response('OK', payload={ serialized_order_data}, status_code=201)