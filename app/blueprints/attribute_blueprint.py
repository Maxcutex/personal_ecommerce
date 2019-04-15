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


@attribute_blueprint.route('', methods=['POST'])
@Security.validator(['attributeName|required:string'])
@Auth.has_permission('create_attribute')
@swag_from('documentation/create_single_attribute.yml')
def create_attribute():
	return attribute_controller.create_attribute()


@attribute_blueprint.route('/<int:attribute_id>', methods=['PATCH', 'PUT'])
@Auth.has_permission('update_attribute')
@swag_from('documentation/update_single_attribute.yml')
def update_attribute(attribute_id):
	return attribute_controller.update_attribute(attribute_id)


@attribute_blueprint.route('/<int:attribute_id>', methods=['DELETE'])
@Auth.has_permission('delete_attribute')
@swag_from('documentation/delete_single_attribute.yml')
def delete_attribute(attribute_id):
	return attribute_controller.delete_attribute(attribute_id)
