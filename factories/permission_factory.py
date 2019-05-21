import factory
from app.utils import db
from app.models.permission import Permission
from factories.role_factory import RoleFactory


class PermissionFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = Permission
		sqlalchemy_session = db.session

	id = factory.Sequence(lambda n: n)
	name = factory.Sequence(lambda n: n)
	role_id = factory.SubFactory(RoleFactory)
	keyword = factory.Sequence(lambda n: n)