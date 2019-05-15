from flasgger import swag_from

from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.department_controller import DepartmentController

url_prefix = '{}/departments'.format(BaseBlueprint.base_url_prefix)
department_blueprint = Blueprint('department', __name__, url_prefix=url_prefix)
department_controller = DepartmentController(request)
	
@department_blueprint.route('/', methods=['GET'])
@Auth.has_permission('view_department')
@swag_from('documentation/get_all_departments.yml')
def list_departments():
	return department_controller.list_departments()

@department_blueprint.route('/<int:department_id>', methods=['GET'])
@Auth.has_permission('view_department')
@swag_from('documentation/get_single_department.yml')
def get_department(department_id):
	return department_controller.get_department(department_id)

@department_blueprint.route('/', methods=['POST'])
@Auth.has_role('admin')
@Security.validator(['name|required:ifExists_Department_name', 'description|required'])
@swag_from('documentation/create_department.yml')
def create_department():
	return department_controller.create_department()

@department_blueprint.route('/<int:department_id>', methods=['DELETE'])
@Auth.has_role('admin')
@swag_from('documentation/delete_department.yml')
def delete_department(department_id):
	return department_controller.delete_department(department_id)

@department_blueprint.route('/<int:department_id>', methods=['PATCH'])
@Auth.has_role('admin')
@Security.validator(['name|optional', 'description|optional'])
@swag_from('documentation/create_department.yml')
def update_department(department_id):
	return department_controller.update_department(department_id)
