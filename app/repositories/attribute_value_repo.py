from app.repositories.base_repo import BaseRepo
from app.models.attribute_value import AttributeValue

class AttributeValueRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, AttributeValue)