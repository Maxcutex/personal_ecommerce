from tests.base_test_case import BaseTestCase
from app.models import Customer
from factories import CustomerFactory

class TestCustomerModel(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_accessing_password_attribute_fails(self):
        customer = CustomerFactory.create()

        with self.assertRaises(AttributeError)  as err:
            customer.password

    def test_str_representation(self):
        customer = CustomerFactory.create()

        assert str(customer) == f'<Customer: {customer.name}>'

    def test_repr_representation(self):
        customer = CustomerFactory.create()

        assert repr(customer) == f'<Customer: {customer.name}>'
