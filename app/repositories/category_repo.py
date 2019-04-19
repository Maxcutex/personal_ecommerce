from app.repositories.base_repo import BaseRepo
from app.models.category import Category

class CategoryRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Category)