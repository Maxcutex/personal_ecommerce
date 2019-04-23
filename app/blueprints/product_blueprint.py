from flasgger import swag_from

from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.product_controller import ProductController

url_prefix = '{}/'.format(BaseBlueprint.base_url_prefix)
product_blueprint = Blueprint('product', __name__, url_prefix=url_prefix)
product_controller = ProductController(request)


@product_blueprint.route('', methods=['GET'])
@Auth.has_permission('view_product')
@swag_from('documentation/get_all_products.yml')
def list_products():
	return product_controller.list_products()


@product_blueprint.route('/search', methods=['GET'])
@Auth.has_permission('view_product')
@Security.validator(
	['query_string|required', 'all_words|optional', 'page|optional', 'limit|optional', 'description_length|optional'])
@swag_from('documentation/get_all_products.yml')
def list_products():
	return product_controller.search_product()


@product_blueprint.route('/<int:product_id>', methods=['GET'])
@Auth.has_permission('view_product')
@swag_from('documentation/get_single_product.yml')
def get_product(product_id):
	return product_controller.get_product(product_id)


@product_blueprint.route('/inCategory/<int:category_id>', methods=['GET'])
@Auth.has_permission('view_product')
@swag_from('documentation/get_single_product.yml')
def get_product_in_category(category_id):
	return product_controller.get_product_in_category(category_id)


@product_blueprint.route('/inDepartment/<int:department_id>', methods=['GET'])
@Auth.has_permission('view_product')
@swag_from('documentation/get_single_product.yml')
def get_product_in_department(department_id):
	return product_controller.get_product_in_department(department_id)


@product_blueprint.route('/<int:product_id>/details', methods=['GET'])
@Auth.has_permission('view_product')
@swag_from('documentation/get_single_product.yml')
def get_product_details(product_id):
	return product_controller.get_product_details(product_id)

@product_blueprint.route('/<int:product_id>/locations', methods=['GET'])
@Auth.has_permission('view_product')
@swag_from('documentation/get_single_product.yml')
def get_product_locations(product_id):
	return product_controller.get_product_locations(product_id)


@product_blueprint.route('/<int:product_id>/reviews', methods=['GET'])
@Auth.has_permission('view_product')
@swag_from('documentation/get_single_product.yml')
def get_product_reviews(product_id):
	return product_controller.get_product_reviews(product_id)


@product_blueprint.route('/<int:product_id>/reviews', methods=['POST'])
@Auth.has_permission('view_product')
@swag_from('documentation/get_single_product.yml')
def post_product_reviews(product_id):
	return product_controller.post_product_reviews(product_id)
