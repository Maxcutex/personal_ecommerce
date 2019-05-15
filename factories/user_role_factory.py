import factory
from app.utils import db
from app.models.user_role import UserRole
from factories.role_factory import RoleFactory
from factories.customer_factory import CustomerFactory


class UserRoleFactory(factory.alchemy.SQLAlchemyModelFactory):

	class Meta:
		model = UserRole
		sqlalchemy_session = db.session

	role_id = factory.SubFactory(RoleFactory)
	user_id = factory.SubFactory(CustomerFactory)
