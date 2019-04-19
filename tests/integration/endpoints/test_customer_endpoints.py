from tests.base_test_case import BaseTestCase
from factories import UserFactory


class TestCustomerEndpoints(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()

    def test_create_customer_succeeds(self):
        password = '123456'
        user = UserFactory.build(name="test_user", email='testemail@gmail.com', password=password)


        user_data = dict(name=user.name, email=user.email, password=password)

        response = self.client().post(self.make_url("/customers/"), headers=self.headers(),
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], "OK")
        self.assertEqual(response_json['payload']['user']['name'], user.name)
        self.assertEqual(response_json['payload']['user']['email'], user.email)

    def test_create_customer_with_duplicate_id_fails(self):
        password = '123456'
        user = UserFactory.create(name="test_user", email='testemail@gmail.com', password=password)

        user_data = dict(name=user.name, email=user.email, password=password)

        response = self.client().post(self.make_url("/customers/"), headers=self.headers(),
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['errors']['email'],
            f"Bad Request - Customer with email '{user.email}' already exists.")

    def test_create_customer_with_invalid_data_fails(self):

        user_data = dict(email='invalid_email')

        response = self.client().post(self.make_url("/customers/"), headers=self.headers(),
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))


        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['errors']['email'],
            f"Bad Request - '{user_data.get('email')}' is not a valid email address.")
        self.assertEqual(
            response_json['errors']['password'],
            "Bad Request - password is required")
        self.assertEqual(
            response_json['errors']['name'],
            "Bad Request - name is required")

