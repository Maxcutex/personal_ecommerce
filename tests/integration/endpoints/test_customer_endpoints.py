from unittest.mock import patch
from tests.base_test_case import BaseTestCase
from factories import CustomerFactory
from app.controllers.customer_controller import facebook
from app.controllers.customer_controller import id_token


class TestCustomerEndpoints(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()

    def test_create_customer_succeeds(self):
        password = '123456'
        user = CustomerFactory.build(name="test_user", email='testemail@gmail.com', password=password)


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
        user = CustomerFactory.create(name="test_user", email='testemail@gmail.com', password=password)

        user_data = dict(name=user.name, email=user.email, password=password)

        response = self.client().post(self.make_url("/customers/"), headers=self.headers(),
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['error'][0]['message'],
                         f"Customer with the email '{user.email}' already exists.")

    def test_create_customer_with_invalid_data_fails(self):

        user_data = dict(email='invalid_email')

        response = self.client().post(self.make_url("/customers/"), headers=self.headers(),
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['error'][0]['message'], 'The email is invalid.')
        self.assertEqual(response_json['error'][1]['message'], 'The field(s) are/is required.')
        self.assertEqual(response_json['error'][2]['message'], 'The field(s) are/is required.')

    @patch.object(facebook.GraphAPI, 'request')
    def test_facebook_login_succeeds(self, mock_fb_request):
        user_info = {
            'name': 'testuser',
            'email': 'testuser@gmail.com'
        }

        post_data = dict(accessToken='gsdhsdbnmdbjksdjksd')

        mock_fb_request.return_value = user_info

        response = self.client().post(self.make_url("/customers/facebook"), headers=self.headers(),
                                      data=self.encode_to_json_string(post_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['user']['name'], user_info['name'])
        self.assertEqual(response_json['payload']['user']['email'], user_info['email'])

    @patch.object(id_token, 'verify_oauth2_token')
    def test_google_login_succeeds(self, mock_fb_request):
        user_info = {
            'name': 'testuser',
            'email': 'testuser@gmail.com'
        }

        post_data = dict(accessToken='gsdhsdbnmdbjksdjksd')

        mock_fb_request.return_value = user_info

        response = self.client().post(self.make_url("/customers/google"), headers=self.headers(),
                                      data=self.encode_to_json_string(post_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['user']['name'], user_info['name'])
        self.assertEqual(response_json['payload']['user']['email'], user_info['email'])

    def test_customer_login_succeeds(self):
        password = '123456'
        user = CustomerFactory(name="test_user", email='testemail@gmail.com', password=password)

        user_data = dict(name=user.name, email=user.email, password=password)

        response = self.client().post(self.make_url("/customers/login"), headers=self.headers(),
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], "OK")
        self.assertEqual(response_json['payload']['user']['name'], user.name)
        self.assertEqual(response_json['payload']['user']['email'], user.email)

    def test_update_endpoint_succeeds(self):
        password = '123456'
        user = CustomerFactory(name="test_user", email='testemail@gmail.com', password=password)

        user_data = dict(name="new test user name", address1='new address')

        response = self.client().patch(self.make_url("/customers/"), headers=self.headers(user),
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], "OK")
        self.assertEqual(response_json['payload']['user']['name'], user_data.get('name'))
        self.assertEqual(response_json['payload']['user']['address1'], user_data.get('address1'))

    def test_update_endpoint_with_no_auth_fails(self):

        user_data = dict(name="new test user name", address1='new address')

        response = self.client().patch(self.make_url("/customers/"), data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['error']['message'], "Authorization code is empty.")
