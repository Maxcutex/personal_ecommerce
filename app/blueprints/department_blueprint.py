from flasgger import swag_from

from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.department_controller import DepartmentController

url_prefix = '{}/'.format(BaseBlueprint.base_url_prefix)
department_blueprint = Blueprint('department', __name__, url_prefix=url_prefix)
department_controller = DepartmentController(request)
	
@department_blueprint.route('', methods=['GET'])
@Auth.has_permission('view_department')
@swag_from('documentation/get_all_departments.yml')
def list_departments():
	return department_controller.list_departments()




@department_blueprint.route('/<int:department_id>', methods=['GET'])
@Auth.has_permission('view_department')
@swag_from('documentation/get_single_department.yml')
def get_department(department_id):
	return department_controller.get_department(department_id)