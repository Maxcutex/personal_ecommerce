'''Unit tests for the category controller.
'''
from tests.base_test_case import BaseTestCase
from app.controllers.category_controller import CategoryController, DepartmentRepo
from factories.category_factory import CategoryFactory
from factories.department_factory import DepartmentFactory
from unittest.mock import patch


class TestCategoryController(BaseTestCase):

    @patch.object(DepartmentRepo, 'get')
    @patch.object(CategoryController, 'request_params_dict')
    def test_create_category_succeeds(self, mock_request_params, mock_dept_get):
        with self.app.app_context():
            department = DepartmentFactory(department_id=6)
            category_info = CategoryFactory.build(department_id=department.department_id)
            mock_request_params.return_value = {
                'name': category_info.name,
                'description': category_info.description,
                'department_id': category_info.department_id
            }
            mock_dept_get.return_value = True

            category_controller = CategoryController(self.request_context)

            # Act
            result = category_controller.create_category()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'

    @patch.object(DepartmentRepo, 'get')
    @patch.object(CategoryController, 'request_params_dict')
    def test_create_category_with_invalid_department_id_fails(self, mock_request_params, mock_dept_get):
        with self.app.app_context():
            mock_request_params.return_value = {
                'name': 'test name',
                'description': 'test description',
                'department_id': 100
            }

            mock_dept_get.return_value = False

            category_controller = CategoryController(self.request_context)

            # Act
            result = category_controller.create_category()

            # Assert
            assert result.status_code == 404
            assert result.get_json()['error']['message'] == "Department with given ID doesn't exist"
