from app.repositories.base_repo import BaseRepo
from app.models.tax import Tax

class TaxRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Tax)