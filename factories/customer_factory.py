import factory
from app.utils import db
from app.models.customer import Customer
from factories.department_factory import DepartmentFactory


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Customer
        sqlalchemy_session = db.session

    customer_id = factory.Sequence(lambda n: n)
    name = 'Surname'
    email = factory.Faker('email')
    address_1 = factory.Faker('address')
    address_2 = factory.Faker('address')
    city = factory.Faker('city')
    region = factory.Faker('city')
    postal_code = "00345"
    country = factory.Faker('country')
    shipping_region_id = 1
    day_phone = '555-10101011'
    eve_phone = '555-10101021'
    mob_phone = '555-10101031'
    password_hash = factory.Faker('password')

