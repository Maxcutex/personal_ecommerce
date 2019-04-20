from app.controllers.base_controller import BaseController
from app.repositories.tax_repo import TaxRepo


class TaxController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.tax_repo = TaxRepo()

	def list_taxes(self):

		taxes = self.tax_repo.get_unpaginated_asc(
			self.tax_repo._model.name,
			is_deleted=False
		)
		taxes_list = [tax.serialize() for tax in taxes]
		return self.handle_response('OK', payload={taxes_list})

	def list_taxes_page(self, page_id, taxes_per_page):

		taxes = self.tax_repo.filter_by(page=page_id, per_page=taxes_per_page, is_deleted=False)
		taxes_list = [tax.serialize() for tax in taxes.items]
		return self.handle_response('OK',
									payload={'taxes': taxes_list, 'meta': self.pagination_meta(taxes)})

	def get_tax(self, tax_id):
		tax = self.tax_repo.get(tax_id)
		if tax:
			if tax.is_deleted:
				return self.handle_response('Bad Request. This tax not longer exists', status_code=400)
			tax = tax.serialize()
			return self.handle_response('OK', payload={'tax': tax})
		else:
			return self.handle_response('Bad Request. This tax id does not exist', status_code=400)