from app.repositories.base_repo import BaseRepo
from app.models.product_rating import ProductRating


class ProductRatingRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, ProductRating)

    def new_rating(self, product_id, user_id, rating, service_date, rating_type, type_id, engagement_id, main_menu_id, channel='web', comment=''):
        product_rating = ProductRating(
            product_id=product_id, user_id=user_id,
            rating=rating,  channel=channel, comment=comment
        )
        product_rating.save()
        return product_rating

