from tests.base_test_case import BaseTestCase
from factories import AttributeFactory, RoleFactory, PermissionFactory, UserRoleFactory


class TestMealItemEndpoints(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()

	def test_create_attributes_endpoint_without_right_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='wrong_permission', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.build()
		data = {'attributeName': attributes.name}
		response = self.client().post(self.make_url('/attributes'), data=self.encode_to_json_string(data),
									  headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Access Error - Permission Denied')

	def test_create_attributes_endpoint_with_right_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='create_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.build()
		data = {'attributeName': attributes.name}
		response = self.client().post(self.make_url('/attributes'), data=self.encode_to_json_string(data),
									  headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assertEqual(response.status_code, 201)
		self.assertJSONKeyPresent(response_json, 'payload')
		self.assertEqual(payload['attribute']['name'], attributes.name)

	def test_create_attributes_endpoint_with_missing_name(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='create_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.build()
		data = {}
		response = self.client().post(self.make_url('/attributes'), data=self.encode_to_json_string(data),
									  headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Bad Request - name is required')


	def test_create_attributes_endpoint_with_existing_name(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='create_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		AttributeFactory.create(name='Color')
		attributes = AttributeFactory.build(name='Color')
		data = {'attributeName': attributes.name}
		response = self.client().post(self.make_url('/attributes'), data=self.encode_to_json_string(data),
									  headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'attribute item with this name already exists')

	def test_list_attributes_endpoint_right_permission(self):
		# Create Three Dummy Vendors
		attributes = AttributeFactory.create_batch(3)

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='view_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().get(self.make_url('/attributes'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(len(payload['attributes']), 3)
		self.assertJSONKeysPresent(payload['attributes'][0], 'name')

	def test_list_attributes_endpoint_correct_sort_order(self):
		# Create Three Dummy Vendors
		attributes = AttributeFactory.create_batch(3)

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='view_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().get(self.make_url('/attributes'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		attributes_sorted_by_name = sorted(
			[meal.name for meal in attributes]
		)

		attributes_returned = [meal.get("name") for meal in payload['attributes']]

		self.assert200(response)
		self.assertEqual(len(payload['attributes']), 3)
		self.assertJSONKeysPresent(payload['attributes'][0], 'name')
		self.assertEqual(attributes_returned[0], attributes_sorted_by_name[0])
		self.assertEqual(attributes_returned[1], attributes_sorted_by_name[1])
		self.assertEqual(attributes_returned[2], attributes_sorted_by_name[2])

	def test_list_attributes_endpoint_wrong_permission(self):
		# Create Three Dummy Vendors
		attribute = AttributeFactory.create_batch(3)

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='wrong_permission', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().get(self.make_url('/attributes'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Access Error - Permission Denied')

	def test_get_specific_attributes_enpoint_right_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='view_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.create()

		response = self.client().get(self.make_url('/attributes/{}'.format(attributes.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertJSONKeyPresent(payload, 'attribute')
		self.assertJSONKeysPresent(payload['attribute'], 'name', 'description', 'mealType', 'image')
		self.assertEqual(int(payload['attribute']['id']), attributes.id)
		self.assertEqual(payload['attribute']['name'], attributes.name)


	def test_get_specific_attributes_endpoint_wrong_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='wrong_permission', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.create()

		response = self.client().get(self.make_url('/attributes/{}'.format(attributes.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Access Error - Permission Denied')

	def test_get_specific_attributes_enpoint_wrong_attributes_id(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='view_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.create()

		response = self.client().get(self.make_url('/attributes/100'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Bad Request. This attribute id does not exist')

	def test_get_specific_attributes_enpoint_deleted_attributes_id(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='view_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.create(is_deleted=True)

		response = self.client().get(self.make_url('/attributes/{}'.format(attributes.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Bad Request. This attribute item is deleted')

	def test_update_attributes_endpoint_right_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='update_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.create()
		data = {'attributeName': 'Color'}
		response = self.client().put(
			self.make_url('/attributes/{}'.format(attributes.id)),
			data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['attribute']['name'], data['attributeName'])


	def test_update_attributes_endpoint_wrong_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='wrong_permission', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.create()
		data = {'attributeName': 'Size'}
		response = self.client().put(
			self.make_url('/attributes/{}'.format(attributes.id)),
			data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Access Error - Permission Denied')

	def test_update_attributes_endpoint_to_existing_name(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='update_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes1 = AttributeFactory.create(name='Color')
		attributes = AttributeFactory.create()
		data = {'attributeName': attributes1.name}
		response = self.client().put(
			self.make_url('/attributes/{}'.format(attributes.id)),
			data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'attribute item with this name already exists')

	def test_update_attributes_endpoint_invalid_id(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='update_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attribute = AttributeFactory.create()
		data = {'attributeName': 'Color'}
		response = self.client().put(
			self.make_url('/attributes/100'),
			data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Invalid or incorrect attribute_id provided')

	def test_update_deleted_attributes(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='update_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.create(is_deleted=True)
		data = {'attributeName': 'Size'}
		response = self.client().put(self.make_url('/attributes/{}'.format(attributes.id)),
									 data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Bad Request. This attribute item is deleted')

	def test_delete_attributes_endpoint_right_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.create()

		response = self.client().delete(self.make_url('/attributes/{}'.format(attributes.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['status'], "success")

	def test_delete_attributes_enpoint_wrong_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='wrong_permission', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.create()

		response = self.client().delete(self.make_url('/attributes/{}'.format(attributes.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Access Error - Permission Denied')

	def test_delete_attributes_enpoint_wrong_attributes_id(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.create()

		response = self.client().delete(self.make_url('/attributes/100'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Invalid or incorrect attribute_id provided')

	def test_delete_attributes_enpoint_deleted_attributes_id(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_attributes', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		attributes = AttributeFactory.create(is_deleted=True)

		response = self.client().delete(self.make_url('/attributes/{}'.format(attributes.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Bad Request. This attribute item is deleted')

