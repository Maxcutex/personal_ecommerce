from app.repositories.base_repo import BaseRepo
from app.models.order import Order

class OrderRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Order)

	def new_order(self, **kwargs):


		order = Order(**kwargs)
		order.save()
		return order