from flasgger import swag_from

from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.category_controller import CategoryController

url_prefix = '{}/categories'.format(BaseBlueprint.base_url_prefix)
category_blueprint = Blueprint('categories', __name__, url_prefix=url_prefix)
category_controller = CategoryController(request)


@category_blueprint.route('', methods=['GET'])
@Auth.has_permission('view_category')
@swag_from('documentation/get_all_categories.yml')
def list_categories():
	return category_controller.list_categories()


@category_blueprint.route('/<int:category_id>', methods=['GET'])
@Auth.has_permission('view_category')
@swag_from('documentation/get_single_category.yml')
def get_category(category_id):
	return category_controller.get_category(category_id)


@category_blueprint.route('/inDepartment/<int:department_id>', methods=['GET'])
@Auth.has_permission('view_category')
@swag_from('documentation/get_category_department.yml')
def get_category_department(department_id):
	return category_controller.get_category_department(department_id)


@category_blueprint.route('/inProduct/<int:product_id>', methods=['GET'])
@Auth.has_permission('view_category')
@swag_from('documentation/get_category_in_product.yml')
def get_categorys_in_product(product_id):
	return category_controller.get_category_product(product_id)

@category_blueprint.route('/', methods=['POST'])
@Auth.has_role('admin')
@Security.validator(['name|required:ifExists_Category_name', 'description|required', 'departmentId|required'])
@swag_from('documentation/create_category.yml')
def create_category():
	return category_controller.create_category()
