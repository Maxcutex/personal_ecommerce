from app.repositories.base_repo import BaseRepo
from app.models.order_detail import OrderDetail

class OrderDetailRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, OrderDetail)


	def new_order_detail(self, **kwargs):


		order_detail = OrderDetail(**kwargs)
		order_detail.save()
		return order_detail