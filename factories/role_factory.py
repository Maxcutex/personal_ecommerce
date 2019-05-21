import factory
from app.utils import db
from app.models.role import Role


class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = Role
		sqlalchemy_session = db.session

	role_id = factory.Sequence(lambda n: n)
	name = factory.Sequence(lambda n: n)
	description = 'A Help Message'

