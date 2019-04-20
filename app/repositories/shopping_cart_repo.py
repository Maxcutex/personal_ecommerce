from app.repositories.base_repo import BaseRepo
from app.models.shopping_cart import ShoppingCart

class ShoppingCartRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, ShoppingCart)

	def new_cart(self, cart_id, product_id, attributes, quantity, buy_now, added_on):
		cart = ShoppingCart(
			cart_id=cart_id, product_id=product_id, attributes=attributes,
			quantity=quantity, buy_now=buy_now, added_on=added_on
		)
		cart.save()
		return cart
