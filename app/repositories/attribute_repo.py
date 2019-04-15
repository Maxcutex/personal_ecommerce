from app.repositories.base_repo import BaseRepo
from app.models.attribute import Attribute


class AttributeRepo(BaseRepo):

	def __init__(self):
		BaseRepo.__init__(self, Attribute)

	def new_attribute(self, name):
		atrribute = Attribute(name=name)
		atrribute.save()
		return atrribute


