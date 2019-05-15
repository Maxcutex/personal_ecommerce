from tests.base_test_case import BaseTestCase, fake

from factories import RoleFactory, UserRoleFactory, PermissionFactory


def create_user_role(role_name, perm_keyword=fake.name()):
    role = RoleFactory.create(name=role_name)
    user_id = BaseTestCase.user_id()
    PermissionFactory.create(name=perm_keyword, keyword=perm_keyword, role_id=role.role_id)

    return UserRoleFactory.create(user_id=user_id, role_id=role.role_id), user_id