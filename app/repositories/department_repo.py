from app.repositories.base_repo import BaseRepo
from app.models.department import Department

class DepartmentRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Department)

	def new_department(self, name, description):

		department = Department(name=name, description=description)
		department.save()

		return department