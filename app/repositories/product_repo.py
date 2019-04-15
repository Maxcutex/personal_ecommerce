from app.repositories.base_repo import BaseRepo
from app.models import Product, ProductRating


class ProductRepo(BaseRepo):

	def __init__(self):
		BaseRepo.__init__(self, Product)

	def new_product(self, name, address, tel, is_active, contact_person, location_id):
		product = Product(name=name, address=address, tel=tel, is_active=is_active, contact_person=contact_person,
						location_id=location_id)
		product.save()
		return product

	def update_Product_average_rating(self, product_id):
		product_ratings = ProductRating.query.filter_by(product_id=product_id).all()
		product = self.get(product_id)
		rating_values = [rating.rating for rating in product_ratings]
		rating_sum = sum(rating_values)
		average = round(rating_sum / len(rating_values), 1)
		self.update(Product, average_rating=average)
		return average
