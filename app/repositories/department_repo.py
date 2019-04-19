from app.repositories.base_repo import BaseRepo
from app.models.department import Department

class DepartmentRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Department)