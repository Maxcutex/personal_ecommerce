from app.controllers.base_controller import BaseController
from app.repositories import UserRoleRepo, RoleRepo, CustomerRepo
from app.models import Role, Customer
from app.utils.auth import Auth

class UserController(BaseController):
    '''
    User Controller.
    '''

    def __init__(self, request):
        '''
        Constructor.
        Parameters:
        -----------
            request
        '''

        BaseController.__init__(self, request)
        self.user_role_repo = UserRoleRepo()
        self.role_repo = RoleRepo()
        self.customer_repo = CustomerRepo()

    def list_admin_users(self, admin_role_id: int = 1) -> list:
        '''
        List admin users.
        Parameters:
        -----------
        admin_role_id {int}
            Admin role ID (default: {1}).
        Returns:
        --------
        list
            List of admin users' profiles.
        '''

        user_roles = self.user_role_repo.filter_by(
            role_id=admin_role_id,
            is_active=True
        ).items

        admin_users_list = []
        for user_role in user_roles:
            admin_user_profile = {}

            associated_roles = [user_role.role_id for user_role in
                                self.user_role_repo.filter_by(user_id=user_role.user_id).items]
            user_objects = Customer.query.filter(Customer.id.in_(associated_roles)).all()
            users = [{'id': user.id, 'first_name': user.first_name} for user in user_objects]

            admin_users_list.append(users)

        return self.handle_response(
            'OK',
            payload={'AdminUsers': admin_users_list}
        )

    def list_all_users(self):

        params = self.get_params_dict()
        pg = int(params.get('page', 1))
        pp = int(params.get('per_page', 10))

        users = self.customer_repo.paginate(error_out=False, page=pg, per_page=pp)
        if users.items:
            user_list = [user.serialize() for user in users.items]
            for user in user_list:
                associated_roles = [user_role.role_id for user_role in
                                    self.user_role_repo.filter_by(user_id=user['userId']).items]
                role_objects = Role.query.filter(Role.id.in_(associated_roles)).all()
                roles = [{'id': role.id, 'name': role.name} for role in role_objects]
                user['userRoles'] = roles
            return self.handle_response('OK', payload={'users': user_list, 'meta': self.pagination_meta(users)})
        return self.handle_response('No users found', status_code=404)

    def delete_user(self, id):
        user = self.customer_repo.get(id)
        if user:
            if user.is_deleted:
                return self.handle_response('User has already been deleted', status_code=400)

            updates = {}
            updates['is_deleted'] = True

            self.customer_repo.update(user, **updates)

            return self.handle_response('User deleted', payload={"status": "success"})
        return self.handle_response('Invalid or incorrect id provided', status_code=404)

    def create_user(self):

        user_info = self.request_params_dict(
            'email', 'name', 'password', 'address1', 'address2', 'city','region', 'postalCode',
            'country', 'shippingRegionId', 'dayPhone', 'evePhone', 'mobPhone')

        user = self.customer_repo.new_user(**user_info)
        token = Auth.generate_token(user.serialize(exclude=('timestamps','is_deleted')))
        serialized_user_data = user.serialize()

        serialized_user_data.__setitem__('token', token)

        return self.handle_response('OK', payload={'user': serialized_user_data}, status_code=201)

    def list_user(self, email):

        user = self.customer_repo.find_first(email=email)
        if user:
            return self.handle_response('OK', payload={'user': user.serialize()}, status_code=200)
        return self.handle_response('User not found', status_code=404)

    def update_user(self, email):
        user = self.customer_repo.get(email)

        if not user:
            return self.handle_response(
                msg="FAIL",
                payload={'user': 'User not found'}, status_code=404
            )

        if user.is_deleted:
            return self.handle_response(
                msg="FAIL",
                payload={'user': 'User already deleted'}, status_code=400
            )

        user_info = self.request_params_dict('email', 'firstName', 'lastName', 'id')

        user = self.customer_repo.update(user, **user_info)

        return self.handle_response('OK', payload={'user': user.serialize()}, status_code=200)
