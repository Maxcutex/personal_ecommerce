from app.repositories.base_repo import BaseRepo
from app.models.category import Category

class CategoryRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Category)

	def new_category(self, name, description, department_id):
		category = Category(name=name, description=description, department_id=department_id)
		category.save()
		return category
