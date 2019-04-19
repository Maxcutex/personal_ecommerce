from app.repositories.base_repo import BaseRepo
from app.models.customer import Customer


class CustomerRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, Customer)

    def new_user(self, **kwargs):
        """
        function for creating a new customer

        :parameter
            kwargs: a dictionary containing the following keys
                  [
                    name, email, address_1, address_1, city, region, postal_code, country,
                    shipping_region_id, day_phone, eve_phone, mob_phone, password_hash
                  ]

        """

        customer = Customer(**kwargs)
        customer.save()
        return customer
