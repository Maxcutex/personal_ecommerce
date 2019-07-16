import factory
from app.utils import db
from app.models.category import Category
from factories.department_factory import DepartmentFactory


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session = db.session

    category_id = factory.Sequence(lambda n: n)
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    department_id = factory.Sequence(lambda n: n)
