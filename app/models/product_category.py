from .base_model import BaseModel, db

class ProductCategory(BaseModel):
	__tablename__ = 'product_categories'

	product_id = db.Column(db.Integer(), db.ForeignKey('products.id'), default=1)
	product = db.relationship('Product', lazy=False)
	category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'), default=1)
	category = db.relationship('Category', lazy=False)