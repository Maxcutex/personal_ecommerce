import pdb

from app import Auth
from app.controllers.base_controller import BaseController
from app.repositories.attribute_repo import AttributeRepo
from app.repositories.attribute_value_repo import AttributeValueRepo
from app.repositories.product_attribute_repo import ProductAttributeRepo


class AttributeController(BaseController):

	def __init__(self, request):
		BaseController.__init__(self, request)
		self.attribute_repo = AttributeRepo()
		self.attribute_value_repo = AttributeValueRepo
		self.product_attribute_repo = ProductAttributeRepo

	def list_attributes(self):
		
		attributes = self.attribute_repo.get_unpaginated_asc(
			self.attribute_repo._model.name,
			is_deleted=False
		)
		attributes_list = [attribute.serialize() for attribute in attributes]
		return self.handle_response('OK', payload={'attributes': attributes_list})

	def list_attributes_page(self, page_id, attributes_per_page):
		
		attributes = self.attribute_repo.filter_by(page=page_id, per_page=attributes_per_page)
		attributes_list = [attribute.serialize() for attribute in attributes.items]
		return self.handle_response('OK', payload={'attributes': attributes_list, 'meta': self.pagination_meta(attributes)})

	def get_attribute(self, attribute_id):
		attribute = self.attribute_repo.get(attribute_id)
		if attribute:
			if attribute.is_deleted:
				return self.handle_response('Bad Request. This attribute item is deleted', status_code=400)
			attribute = attribute.serialize()
			return self.handle_response('OK', payload={'attribute': attribute})
		else:
			return self.handle_response('Bad Request. This attribute id does not exist', status_code=400)

	def get_attribute_values(self, attribute_id):
		attribute_values = self.attribute_value_repo.filter_by(attribute_id=attribute_id)
		if attribute_values:
			attribute_values_list = [attribute_value.serialize() for attribute_value in attribute_values]
			return self.handle_response('OK', payload={'attribute': attribute_values_list})
		else:
			return self.handle_response('Bad Request. This attribute values for attribute id does not exist', status_code=400)

	def get_attribute_product(self, product_id):
		product_attributes = self.product_attribute_repo.filter_by(product_id=product_id)
		product_array = []

		if product_attributes:
			for attribute_value_id in product_attributes:
				attribute_object = []
				attribute_value = self.attribute_value_repo.get(attribute_value_id)
				attribute = self.attribute_repo.get(attribute_value.attribute_id)
				attribute_object['attribute_name'] = attribute.name
				attribute_object['attribute_value_id'] = attribute_value.attribute_value_id
				attribute_object['attribute_value'] = attribute_value.name
				product_array.append(attribute_object)

			return self.handle_response('OK', payload={product_array})

		else:
			return self.handle_response('Bad Request. This attributes for this product does not exist', status_code=400)

	def create_attribute(self):
		"""
		Creates a new attribute item
		"""
		
		name = self.request_params('attributeName')
		if self.attribute_repo.get_unpaginated(name=name):
			return self.handle_response('attribute item with this name already exists', status_code=400)
		new_attribute = self.attribute_repo.new_attribute(name).serialize()

		return self.handle_response('OK', payload={'attribute': new_attribute}, status_code=201)

	def update_attribute(self, attribute_id):
		name = self.request_params('attributeName')

		attribute = self.attribute_repo.get(attribute_id)
		if attribute:
			if attribute.is_deleted:
				return self.handle_response('Bad Request. This attribute item is deleted', status_code=400)

			updates = {}
			if name:
				if self.attribute_repo.get_unpaginated(name=name):
					return self.handle_response('attribute item with this name already exists', status_code=400)
				updates['name'] = name

			self.attribute_repo.update(attribute, **updates)
			return self.handle_response('OK', payload={'attribute': attribute.serialize()})

		return self.handle_response('Invalid or incorrect attribute_id provided', status_code=400)

	def delete_attribute(self, attribute_id):
		attribute = self.attribute_repo.get(attribute_id)
		updates = {}
		if attribute:
			if attribute.is_deleted:
				return self.handle_response('Bad Request. This attribute item is deleted', status_code=400)
			updates['is_deleted'] = True

			self.attribute_repo.update(attribute, **updates)
			return self.handle_response('OK', payload={"status": "success"})
		return self.handle_response('Invalid or incorrect attribute_id provided', status_code=400)