'''
Unit tests for the User Controller.
'''
from datetime import datetime
from unittest.mock import patch
from app.controllers.customer_controller import CustomerController, Auth
from app.models.user_role import UserRole
from tests.base_test_case import BaseTestCase
from factories.customer_factory import UserFactory
from app.controllers.customer_controller import facebook
from app.controllers.customer_controller import id_token

class TestUserController(BaseTestCase):
    '''
    CustomerController test class.
    '''

    def setUp(self):
        self.BaseSetUp()
        self.mock_user_role = UserRole(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            role_id=1,
            user_id=1,
            is_active=True
        )

    # @patch('app.repositories.user_role_repo.UserRoleRepo.filter_by')
    # def test_list_admin_users_ok_response(
    #     self,
    #     mock_filter_by
    # ):
    #     '''
    #     Test list_admin_users OK response.
    #     '''
    #     # Arrange
    #     with self.app.app_context():
    #         mock_filter_by.return_value.items = [self.mock_user_role, ]
    #
    #         user_controller = CustomerController(self.request_context)
    #
    #         # Act
    #         result = user_controller.list_admin_users()
    #
    #         # Assert
    #         assert result.status_code == 200
    #         assert result.get_json()['msg'] == 'OK'
    #
    @patch.object(CustomerController, 'request_params_dict')
    def test_create_user_succeeds(self, mock_request_params):

        with self.app.app_context():
            mock_request_params.return_value = {
                'email': "email@email.com",
                'name': "Eno",
                'password': "test_pass"
            }
            user_controller = CustomerController(self.request_context)

            # Act
            result = user_controller.create_user()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'
            # self.assertEqual(result.get_json()['payload']['user']['email'], "email@email.com")
            # self.assertEqual(result.get_json()['payload']['user']['firstName'], "Eno")
            # self.assertEqual(result.get_json()['payload']['user']['lastName'], "Bassey")

    def test_list_user_succeeds(self):

        with self.app.app_context():
            user = UserFactory.create(email="testemail@email.com", password="Complexx@34", name='testname')

            user_controller = CustomerController(self.request_context)

            response = user_controller.list_user(email="testemail@email.com")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['msg'], "OK")
            self.assertEqual(response.get_json()['payload']['user']['email'], user.email)
            self.assertEqual(response.get_json()['payload']['user']['name'], user.name)

    def test_list_user_when_user_found_succeeds(self):
        with self.app.app_context():

            user_controller = CustomerController(self.request_context)

            response = user_controller.list_user(email="tester@test.com")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.get_json()['msg'], 'User not found')

    @patch.object(facebook.GraphAPI, 'request')
    @patch.object(CustomerController, 'request_params_dict')
    def test_login_facebook_succeeds(self, mock_request_params, mock_fb_request):
        with self.app.app_context():
            test_user = {
                'email': "email@email.com",
                'name': "Eno",
            }

            mock_request_params.return_value = {
                'access_token': 'hjgsdbkjbasjdbnhjghjabhgfdyuerjhbfhjgfdjhbfd',
            }

            mock_fb_request.return_value = test_user

            user_controller = CustomerController(self.request_context)

            # Act
            result = user_controller.facebook_login()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'
            self.assertEqual(result.get_json()['payload']['user']['email'], test_user.get('email'))
            self.assertEqual(result.get_json()['payload']['user']['name'],  test_user.get('name'))

    @patch.object(facebook, 'GraphAPI')
    @patch.object(CustomerController, 'request_params_dict')
    def test_login_facebook_raises_exception_with_invalid_access_token(self, mock_request_params, mock_fb_request):
        with self.app.app_context():

            mock_request_params.return_value = {
                'access_token': 'hjgsdbkjbasjdbnhjghjabhgfdyuerjhbfhjgfdjhbfd',
            }

            mock_fb_request.side_effect = facebook.GraphAPIError({})

            user_controller = CustomerController(self.request_context)

            # Act
            result = user_controller.facebook_login()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'error'
            self.assertEqual(result.get_json()['payload']['accessToken'], 'invalid token supplied.')

    @patch.object(facebook.GraphAPI, 'request')
    @patch.object(CustomerController, 'request_params_dict')
    def test_login_facebook_without_email_fails(self, mock_request_params, mock_fb_request):
        with self.app.app_context():
            test_user = {
                'email': None,
                'name': "Eno",
            }

            mock_request_params.return_value = {
                'access_token': 'hjgsdbkjbasjdbnhjghjabhgfdyuerjhbfhjgfdjhbfd',
            }

            mock_fb_request.return_value = test_user

            user_controller = CustomerController(self.request_context)

            # Act
            result = user_controller.facebook_login()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'error'
            self.assertEqual(
                result.get_json()['payload']['accessToken'], 'this account does not have an email address set.')

    @patch.object(id_token, 'verify_oauth2_token')
    @patch.object(CustomerController, 'request_params_dict')
    def test_login_google_succeeds(self, mock_request_params, mock_id_token):
        with self.app.app_context():
            test_user = {
                'email': "email@email.com",
                'name': "Eno",
            }

            mock_request_params.return_value = {
                'access_token': 'hjgsdbkjbasjdbnhjghjabhgfdyuerjhbfhjgfdjhbfd',
            }

            mock_id_token.return_value = test_user

            user_controller = CustomerController(self.request_context)

            # Act
            result = user_controller.google_login()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'
            self.assertEqual(result.get_json()['payload']['user']['email'], test_user.get('email'))
            self.assertEqual(result.get_json()['payload']['user']['name'], test_user.get('name'))

    @patch.object(id_token, 'verify_oauth2_token')
    @patch.object(CustomerController, 'request_params_dict')
    def test_login_google_with_invalid_token_fails(self, mock_request_params, mock_id_token):
        with self.app.app_context():
            test_user = {
                'email': "email@email.com",
                'name': "Eno",
            }

            mock_request_params.return_value = {
                'access_token': 'hjgsdbkjbasjdbnhjghjabhgfdyuerjhbfhjgfdjhbfd',
            }

            mock_id_token.side_effect = ValueError()

            user_controller = CustomerController(self.request_context)

            # Act
            result = user_controller.google_login()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'error'
            self.assertEqual(result.get_json()['payload']['accessToken'], 'invalid or expired token supplied.')

    @patch.object(CustomerController, 'request_params_dict')
    def test_login_succeeds(self, mock_request_params):
        with self.app.app_context():
            login_credentials = {
                'email': 'test_user@email.com',
                'password': "gdjysduiehjds",
                'name': 'test user'
            }

            UserFactory(**login_credentials)

            mock_request_params.return_value = login_credentials

            user_controller = CustomerController(self.request_context)

            # Act
            result = user_controller.login()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'
            self.assertEqual(result.get_json()['payload']['user']['email'], login_credentials.get('email'))
            self.assertEqual(result.get_json()['payload']['user']['name'], login_credentials.get('name'))

    @patch.object(CustomerController, 'request_params_dict')
    def test_login_with_invalid_credentials_fails(self, mock_request_params):
        with self.app.app_context():
            login_credentials = {
                'email': 'test_user@email.com',
                'password': "gdjysduiehjds",
                'name': 'test user'
            }


            mock_request_params.return_value = login_credentials

            user_controller = CustomerController(self.request_context)

            # Act
            result = user_controller.login()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid email or password'

    @patch.object(Auth, 'user')
    @patch.object(CustomerController, 'request_params_dict')
    def test_update_user_succeeds(self, mock_request_params, mock_auth_user):
        with self.app.app_context():
            customer_info = {
                'email': 'test_user@email.com',
                'password': "gdjysduiehjds",
                'name': 'test user'
            }
            update_info = {
                'name': 'new test user name',
                'address_1': 'new address'
            }

            UserFactory(**customer_info)

            mock_request_params.return_value = update_info

            mock_auth_user.return_value = customer_info.get('email')

            user_controller = CustomerController(self.request_context)

            # Act
            result = user_controller.update_customer()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'
            self.assertEqual(result.get_json()['payload']['user']['name'], update_info.get('name'))
            self.assertEqual(result.get_json()['payload']['user']['address1'], update_info.get('address_1'))

    @patch.object(Auth, 'user')
    @patch.object(CustomerController, 'request_params_dict')
    def test_update_non_existing_user_failss(self, mock_request_params, mock_auth_user):
        with self.app.app_context():
            customer_info = {
                'email': 'test_user@email.com',
                'password': "gdjysduiehjds",
                'name': 'test user'
            }
            update_info = {
                'name': 'new test user name',
                'address_1': 'new address'
            }

            UserFactory(**customer_info)

            mock_request_params.return_value = update_info

            mock_auth_user.return_value = 'unexisting_user@gamil.com'

            user_controller = CustomerController(self.request_context)

            # Act
            result = user_controller.update_customer()

            # Assert
            assert result.status_code == 404
            assert result.get_json()['msg'] == 'User not found'
