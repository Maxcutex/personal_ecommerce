'''
Unit tests for the User Controller.
'''
import pdb
from datetime import datetime
from unittest.mock import patch

from app import db
from app.controllers.customer_controller import UserController
from app.models.user_role import UserRole
from tests.base_test_case import BaseTestCase
from factories.customer_factory import UserFactory


class TestUserController(BaseTestCase):
    '''
    UserController test class.
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
    #         user_controller = UserController(self.request_context)
    #
    #         # Act
    #         result = user_controller.list_admin_users()
    #
    #         # Assert
    #         assert result.status_code == 200
    #         assert result.get_json()['msg'] == 'OK'
    #
    @patch.object(UserController, 'request_params_dict')
    def test_create_user_succeeds(self, mock_request_params):

        with self.app.app_context():
            mock_request_params.return_value = {
                'email': "email@email.com",
                'name': "Eno",
                'password': "test_pass"
            }
            user_controller = UserController(self.request_context)

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

            user_controller = UserController(self.request_context)

            response = user_controller.list_user(email="testemail@email.com")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['msg'], "OK")
            self.assertEqual(response.get_json()['payload']['user']['email'], user.email)
            self.assertEqual(response.get_json()['payload']['user']['name'], user.name)

    def test_list_user_when_user_found_succeeds(self):
        with self.app.app_context():

            user_controller = UserController(self.request_context)

            response = user_controller.list_user(email="tester@test.com")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.get_json()['msg'], 'User not found')
