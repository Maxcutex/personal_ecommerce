from app.controllers.base_controller import BaseController
from app.repositories.category_repo import CategoryRepo


class CategoryController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.category_repo = CategoryRepo()

	def list_categories(self):

		categories = self.category_repo.get_unpaginated_asc(
			self.category_repo._model.name,
			is_deleted=False
		)
		categories_list = [category.serialize() for category in categories]
		return self.handle_response('OK', payload={'categories': categories_list})

	def list_categories_page(self, page_id, categories_per_page):

		categories = self.category_repo.filter_by(page=page_id, per_page=categories_per_page)
		categories_list = [category.serialize() for category in categories.items]
		return self.handle_response('OK',
									payload={'categories': categories_list, 'meta': self.pagination_meta(categories)})

	def get_category(self, category_id):
		category = self.category_repo.get(category_id)
		if category:
			if category.is_deleted:
				return self.handle_response('Bad Request. This category item is deleted', status_code=400)
			category = category.serialize()
			return self.handle_response('OK', payload={'category': category})
		else:
			return self.handle_response('Bad Request. This category id does not exist', status_code=400)
	
	def get_category_product(self, product_id):
		product_categories = self.product_category_repo.filter_by(product_id=product_id)
		product_array = []

		if product_categories:
			for category_id in product_categories:
				category_object = []
				category = self.category_repo.get(category_id)
				category_object['category_id'] = category.category_id
				category_object['department_id'] = category.department_id
				category_object['name'] = category.name
				product_array.append(category_object)

			return self.handle_response('OK', payload={product_array})

		else:
			return self.handle_response('Bad Request. This categories for this product does not exist', status_code=400)
	
	def get_category_department(self, department_id):
		department_categories = self.category_repo.filter_by(department_id=department_id)
		department_category_array = []

		if department_categories:
			for category_id in department_categories:
				category_object = []
				category = self.category_repo.get(category_id)
				category_object['name'] = category.name
				category_object['department_id'] = category.department_id
				category_object['description'] = category.description
				department_category_array.append(category_object)

			return self.handle_response('OK', payload={department_category_array})

		else:
			return self.handle_response('Bad Request. This categories for this department does not exist', status_code=400)
