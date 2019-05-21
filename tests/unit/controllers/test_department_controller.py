'''
Unit tests for the Department Controller.
'''
from unittest.mock import patch
from app.controllers.department_controller import DepartmentController
from tests.base_test_case import BaseTestCase
from factories import DepartmentFactory


class TestDepartmentController(BaseTestCase):
    '''
    DepartmentController test class.
    '''

    def setUp(self):
        self.BaseSetUp()

    @patch.object(DepartmentController, 'request_params_dict')
    def test_create_department_succeeds(self, mock_request_params):
        with self.app.app_context():
            mock_request_params.return_value = {
                'name': "eastern",
                'description': "test description",
            }
            department_controller = DepartmentController(self.request_context)

            # Act
            result = department_controller.create_department()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'
            self.assertEqual(
                result.get_json()['payload']['department']['name'], "eastern"
            )
            self.assertEqual(
                result.get_json()['payload']['department']['description'], "test description"
            )

    def test_delete_department_succeeds(self):
        with self.app.app_context():
            department = DepartmentFactory.create(name="test")

            department_controller = DepartmentController(self.request_context)

            # Act
            result = department_controller.delete_department(department.department_id)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'Department successfully deleted'

    def test_delete_department_fails(self):
        with self.app.app_context():

            department_controller = DepartmentController(self.request_context)

            # Act
            result = department_controller.delete_department(department_id=6)

            # Assert
            assert result.status_code == 404
            assert result.get_json()['msg'] == 'Department not found'
