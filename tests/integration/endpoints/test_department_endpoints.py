from tests.base_test_case import BaseTestCase
from factories import DepartmentFactory
from tests import create_user_role


class TestDepartmentEndpoints(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()

    def test_create_department_succeeds(self):
        department = DepartmentFactory.build()

        create_user_role('admin')

        department_data = dict(name=department.name, description=department.description)

        response = self.client().post(self.make_url("/departments/"), headers=self.headers(),
                                      data=self.encode_to_json_string(department_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        print('response', response_json)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], "OK")
        self.assertEqual(response_json['payload']['department']['name'], department.name)
        self.assertEqual(response_json['payload']['department']['description'], department.description)

    def test_delete_department_succeeds(self):
        department = DepartmentFactory()

        create_user_role('admin')

        response = self.client().delete(self.make_url(f"/departments/{department.department_id}"),
                                        headers=self.headers(),)

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], "Department successfully deleted")


    def test_update_department_succeeds(self):
        department = DepartmentFactory()

        create_user_role('admin')

        department_data = dict(name='new_test_name')

        response = self.client().patch(self.make_url(f"/departments/{department.department_id}"), headers=self.headers(),
                                      data=self.encode_to_json_string(department_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], "OK")
        self.assertEqual(response_json['payload']['department']['name'], 'new_test_name')
