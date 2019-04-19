from app.repositories.base_repo import BaseRepo
from app.models.customer import Customer


class UserRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, Customer)

    def new_user(self, *args):
        """
        function for creating a new user

        :parameter
            args: a list containing the following positional values
                  [slack_id, first_name, last_name, email, user_id, photo]

        """

        first_name, last_name, email, password, is_admin = args

        user = Customer(first_name=first_name, last_name=last_name,
                    is_admin=is_admin, email=email, password=password)
        user.save()
        return user
