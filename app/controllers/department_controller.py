from app.controllers.base_controller import BaseController
from app.repositories.department_repo import DepartmentRepo


class DepartmentController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.department_repo = DepartmentRepo()

	def list_departments(self):

		departments = self.department_repo.get_unpaginated_asc(
			self.department_repo._model.name,
			is_deleted=False
		)
		departments_list = [department.serialize() for department in departments]
		return self.handle_response('OK', payload={ departments_list})

	def list_departments_page(self, page_id, departments_per_page):

		departments = self.department_repo.filter_by(page=page_id, per_page=departments_per_page, is_deleted=False)
		departments_list = [department.serialize() for department in departments.items]
		return self.handle_response('OK',
									payload={'departments': departments_list, 'meta': self.pagination_meta(departments)})

	def get_department(self, department_id):
		department = self.department_repo.get(department_id)
		if department:
			if department.is_deleted:
				return self.handle_response('Bad Request. This department not longer exists', status_code=400)
			department = department.serialize()
			return self.handle_response('OK', payload={'department': department})
		else:
			return self.handle_response('Bad Request. This department id does not exist', status_code=400)