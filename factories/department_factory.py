import factory
from app.utils import db
from app.models.department import Department


class DepartmentFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = Department
		sqlalchemy_session = db.session

	id = factory.Sequence(lambda n: n)
	name = factory.Faker('word')
	description = 'A Help Message'

