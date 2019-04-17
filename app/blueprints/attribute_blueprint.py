from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request, Auth
from app.controllers.attribute_controller import AttributeController
from flasgger import swag_from

url_prefix = '{}/attributes'.format(BaseBlueprint.base_url_prefix)
attribute_blueprint = Blueprint('attribute', __name__, url_prefix=url_prefix)
attribute_controller = AttributeController(request)


@attribute_blueprint.route('', methods=['GET'])
@Auth.has_permission('view_attribute')
@swag_from('documentation/get_all_attributes.yml')
def list_attributes():
	return attribute_controller.list_attributes()




@attribute_blueprint.route('/<int:attribute_id>', methods=['GET'])
@Auth.has_permission('view_attribute')
@swag_from('documentation/get_single_attribute.yml')
def get_attribute(attribute_id):
	return attribute_controller.get_attribute(attribute_id)


@attribute_blueprint.route('/values/<int:attribute_id>', methods=['GET'])
@Auth.has_permission('view_attribute')
@swag_from('documentation/get_attribute_values.yml')
def get_attribute_values(attribute_id):
	return attribute_controller.get_attribute_values(attribute_id)


@attribute_blueprint.route('/inProduct/<int:product_id>', methods=['GET'])
@Auth.has_permission('view_attribute')
@swag_from('documentation/get_attribute_in_product.yml')
def get_attributes_in_product(product_id):
	return attribute_controller.get_attribute_product(product_id)


