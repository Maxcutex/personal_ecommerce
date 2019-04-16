from app.repositories.base_repo import BaseRepo
from app.models.product_attribute import ProductAttribute


class ProductAttributeRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, ProductAttribute)

	def new_product_attribute(self, product_id, attribute_value_id):
		product_attribute = ProductAttribute(
			product_id=product_id, attribute_value_id=attribute_value_id
		)
		product_attribute.save()
		return product_attribute


