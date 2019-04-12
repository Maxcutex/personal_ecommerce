import factory
from app.utils import db
from app.models.user import User
from factories.department_factory import DepartmentFactory


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    first_name = 'Test'
    last_name = 'Surname'
    email = factory.Faker('email')
    department_id = factory.SubFactory(DepartmentFactory)
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
    is_admin = db.Column(db.Boolean, default=False)

