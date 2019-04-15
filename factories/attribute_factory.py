import factory
from app.utils import db
from app.models.attribute import Attribute


class AttributeFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = Attribute
		sqlalchemy_session = db.session

	id = factory.sequence(lambda n: n)
	name = factory.Faker('name')

