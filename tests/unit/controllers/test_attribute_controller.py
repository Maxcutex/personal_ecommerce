'''Unit tests for the attribute item controller.
'''
from datetime import datetime
from unittest.mock import patch

from app.controllers.attribute_controller import AttributeController
from app.models import Attribute
from app.repositories.attribute_repo import AttributeRepo
from tests.base_test_case import BaseTestCase


class TestAttributeController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.mock_attribute = Attribute(
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name='Mock attribute item'
        )
        self.mock_deleted_attribute = Attribute(
            is_deleted=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name='Mock attribute item'
        )

    @patch.object(AttributeRepo, 'get_unpaginated')
    def test_list_attributes_ok_response(
        self,
        mock_get_unpaginated
    ):
        '''Test list_attributes OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_get_unpaginated.return_value = [self.mock_attribute, ]
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.list_attributes()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(AttributeRepo, 'filter_by')
    @patch.object(AttributeController, 'pagination_meta')
    def test_list_attributes_page_ok_response(
        self,
        mock_pagination_meta,
        mock_filter_by
    ):
        '''Test list_attributes_page OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_filter_by.return_value.items = [self.mock_attribute, ]
            mock_pagination_meta.return_value = {
                'total_rows': 1,
                'total_pages': 1,
                'current_page': 1,
                'next_page': 1,
                'prev_page': 1
            }
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.list_attributes_page(1, 10)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(AttributeRepo, 'get')
    def test_get_attribute_when_attribute_doesnot_exist(
        self,
        mock_get
    ):
        '''Test get_attribute when attribute item doesn't exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_get.return_value = None
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.get_attribute(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Bad Request. This attribute id ' \
                'does not exist'

    @patch.object(AttributeRepo, 'get')
    def test_get_attribute_when_attribute_is_deleted(
        self,
        mock_get
    ):
        '''Test get_attribute when attribute is deleted.
        '''
        # Arrange
        with self.app.app_context():
            mock_get.return_value = self.mock_deleted_attribute
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.get_attribute(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Bad Request. This attribute item' \
                ' is deleted'

    @patch.object(AttributeRepo, 'get')
    def test_get_attribute_ok_response(
        self,
        mock_get
    ):
        '''Test get_attribute OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_get.return_value = self.mock_attribute
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.get_attribute(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(AttributeController, 'request_params')
    @patch.object(AttributeRepo, 'get_unpaginated')
    def test_create_attribute_when_attribute_already_exists(
        self,
        mock_get_unpaginated,
        mock_request_params
    ):
        '''Test create_attribute when the attribute already exists.
        '''
        # Arrange
        with self.app.app_context():
            mock_request_params.return_value = (
                'Mock'
            )
            mock_get_unpaginated.return_value = self.mock_attribute
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.create_attribute()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'attribute item with this name ' \
                'already exists'


    @patch.object(AttributeRepo, 'new_attribute')
    @patch.object(AttributeController, 'request_params')
    @patch.object(AttributeRepo, 'get_unpaginated')
    def test_create_attribute_ok_response(
        self,
        mock_get_unpaginated,
        mock_request_params,
        mock_new_attribute
    ):
        '''Test create_attribute OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_request_params.return_value = (
                'Mock'
            )
            mock_get_unpaginated.return_value = None
            mock_new_attribute.return_value = self.mock_attribute
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.create_attribute()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'

    @patch.object(AttributeController, 'request_params')
    @patch.object(AttributeRepo, 'get')
    def test_update_attribute_when_attribute_doesnot_exist(
        self,
        mock_get,
        mock_request_params
    ):
        '''Test update_attribute when the attribute doesnot exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_request_params.return_value = ('Mock')
            mock_get.return_value = None
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.update_attribute(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect attribute_id' \
                ' provided'

    @patch.object(AttributeController, 'request_params')
    @patch.object(AttributeRepo, 'get')
    def test_update_attribute_when_attribute_is_deleted(
        self,
        mock_get,
        mock_request_params
    ):
        '''Test update_attribute when the attribute is deleted.
        '''
        # Arrange
        with self.app.app_context():
            mock_get.return_value = self.mock_deleted_attribute
            mock_request_params.return_value = ('Mock')
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.update_attribute(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Bad Request. This attribute item ' \
                'is deleted'

    @patch.object(AttributeController, 'request_params')
    @patch.object(AttributeRepo, 'get')
    @patch.object(AttributeRepo, 'get_unpaginated')
    def test_update_attribute_when_name_already_exists(
        self,
        mock_get_unpaginated,
        mock_get,
        mock_request_params
    ):
        '''Test update_attribute when attribute name already exists.
        '''
        # Arrange
        with self.app.app_context():
            mock_request_params.return_value = ('mock')
            mock_get.return_value = self.mock_attribute
            mock_get_unpaginated.return_value = self.mock_attribute
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.update_attribute(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'attribute item with this name ' \
                'already exists'

    @patch.object(AttributeController, 'request_params')
    @patch.object(AttributeRepo, 'get')
    @patch.object(AttributeRepo, 'get_unpaginated')
    def test_update_attribute_ok_response(
        self,
        mock_get_unpaginated,
        mock_get,
        mock_request_params
    ):
        '''Test update_attribute OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_get.return_value = self.mock_attribute
            mock_request_params.return_value = ('mock')
            mock_get_unpaginated.return_value = None
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.update_attribute(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(AttributeRepo, 'get')
    def test_delete_attribute_when_attribute_doesnot_exist(
        self,
        mock_get
    ):
        '''Test delete_attribute when attribute item doesnot exist.
        '''
        with self.app.app_context():
            mock_get.return_value = None
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.delete_attribute(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect attribute_id' \
                ' provided'

    @patch.object(ProductAttributeRepo, 'get')
    def test_get_attributes_of_a_product_by_id(self):
        pass

    @patch.object(AttributeRepo, 'get')
    def test_delete_attribute_when_attribute_is_already_deleted(
        self,
        mock_get
    ):
        '''Test delete_attribute when the attribute is already deleted.
        '''
        # Arrange
        with self.app.app_context():
            mock_get.return_value = self.mock_deleted_attribute
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.delete_attribute(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Bad Request. This attribute item' \
                ' is deleted'

    @patch.object(AttributeRepo, 'get')
    @patch.object(AttributeRepo, 'update')
    def test_delete_attribute_ok_response(
        self,
        mock_update,
        mock_get
    ):
        '''Test delete_attribute OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_get.return_value = self.mock_attribute
            mock_update.return_value = self.mock_attribute
            attribute_controller = AttributeController(self.request_context)

            # Act
            result = attribute_controller.delete_attribute(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'
