from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Auth, Security
from app.controllers.customer_controller import CustomerController
from flasgger import swag_from

user_blueprint = Blueprint('user', __name__, url_prefix='{}/users'.format(BaseBlueprint.base_url_prefix))
customer_blueprint = Blueprint('customer', __name__, url_prefix='{}/customers'.format(BaseBlueprint.base_url_prefix))
customer_controller = CustomerController(request)


@user_blueprint.route('/admin', methods=['GET'])
@Auth.has_permission('create_user_roles')
@swag_from('documentation/get_all_admin_users.yml')
def list_admin_users():
    return customer_controller.list_admin_users()


@user_blueprint.route('/', methods=['GET'])
@Auth.has_permission('view_users')
@swag_from('documentation/get_all_users.yml')
def list_all_users():
    return customer_controller.list_all_users()


@user_blueprint.route('/customer', methods=['GET'])
@Auth.has_permission('view_users')
@swag_from('documentation/get_customer_by_token.yml')
def get_customer_by_token():
    return customer_controller.get_customer_by_token()


@user_blueprint.route('/<int:id>/', methods=['DELETE'])
@Auth.has_permission('delete_user')
@swag_from('documentation/delete_user.yml')
def delete_user(id):
    return customer_controller.delete_user(id)


@customer_blueprint.route('/', methods=['POST'])
@Security.validator(
    ['email|required:email:ifExists_Customer_email', 'name|required', 'password|required', 'address1|optional', 'address2|optional', 'city|optional',
     'region|optional', 'postalCode|optional', 'country|optional', 'shippingRegionId|optional',
     'dayPhone|optional', 'evePhone|optional', 'mobPhone|optional'])
@swag_from('documentation/create_user.yml')
def create_user():
    return customer_controller.create_user()


@customer_blueprint.route('/login', methods=['POST'])
@Security.validator(['email|required:email', 'password|required'])
def login():
    return customer_controller.login()


@customer_blueprint.route('/facebook', methods=['POST'])
@Security.validator(['accessToken|required'])
def facebook_login():
    return customer_controller.facebook_login()


@customer_blueprint.route('/google', methods=['POST'])
@Security.validator(['accessToken|required'])
def google_login():
    return customer_controller.google_login()


@user_blueprint.route('/<int:user_id>', methods=['PUT'])
@Auth.has_permission('update_user')
@Security.validator(
    ['firstName|required', 'lastName|required',
     'email|required', 'password|required', 'day_phone|optional', 'eve_phone|optional', 'mob_phone|optional'])
@swag_from('documentation/update_user.yml')
def update_user(user_id):
    return customer_controller.update_user(user_id)
