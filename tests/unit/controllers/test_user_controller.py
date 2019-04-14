'''
Unit tests for the User Controller.
'''
import pdb
from datetime import datetime
from unittest.mock import patch

from app.controllers.user_controller import UserController
from app.models.user_role import UserRole
from tests.base_test_case import BaseTestCase
from factories.user_factory import UserFactory


class TestUserController(BaseTestCase):
    '''
    UserController test class.
    '''

    def setUp(self):
        self.BaseSetUp()
        self.mock_user_role = UserRole(
            id=1,
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
    #         user_controller = UserController(self.request_context)
    #
    #         # Act
    #         result = user_controller.list_admin_users()
    #
    #         # Assert
    #         assert result.status_code == 200
    #         assert result.get_json()['msg'] == 'OK'
    #
    @patch.object(UserController, 'request_params')
    def test_create_user_succeeds(self, mock_request_params):

        with self.app.app_context():
            mock_request_params.return_value = [
                "email@email.com",
                "Eno",
                "Bassey",
                "-LXTuXlk2W4Gskt8KTte", False
            ]
            user_controller = UserController(self.request_context)

            # Act
            result = user_controller.create_user()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'
            # self.assertEqual(result.get_json()['payload']['user']['email'], "email@email.com")
            # self.assertEqual(result.get_json()['payload']['user']['firstName'], "Eno")
            # self.assertEqual(result.get_json()['payload']['user']['lastName'], "Bassey")

    @patch.object(UserController, 'request_params')
    def test_create_user_method_handles_user_creation_with_duplicate_email_id(self, mock_request_params):
        with self.app.app_context():
            user = UserFactory(email="factory@factoryemail.com", password="Complexx@34")

            mock_request_params.return_value = [
                user.email,
                "Joseph",
                "Serunjogi",
                "-LXTuXlk2W4Gskt8KTte", False
            ]

            user_controller = UserController(self.request_context)

            response = user_controller.create_user()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.get_json()['msg'],
                "User with email '{}' already exists".format(user.email)
            )

    @patch.object(UserController, 'request_params')
    def test_list_user_succeeds(self, mock_request_params):

        with self.app.app_context():
            user = UserFactory(email="testemail@email.com", password="Complexx@34")

            user_controller = UserController(self.request_context)

            response = user_controller.list_user(email="email@email.com")
            pdb.set_trace()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['msg'], "OK")
            self.assertEqual(response.get_json()['payload']['user']['email'], user.email)
            self.assertEqual(response.get_json()['payload']['user']['firstName'], user.first_name)
            self.assertEqual(response.get_json()['payload']['user']['lastName'], user.last_name)

    # def test_list_user_when_user_found_succeeds(self):
    #     with self.app.app_context():
    #
    #         user_controller = UserController(self.request_context)
    #
    #         response = user_controller.list_user(email="tester@test.com")
    #
    #         self.assertEqual(response.status_code, 404)
    #         self.assertEqual(response.get_json()['msg'], 'User not found')
