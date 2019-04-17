from .base_model import BaseModel, db

class ProductCategory(BaseModel):
	__tablename__ = 'product_categories'

	product_id = db.Column(db.Integer(),  db.ForeignKey('products.product_id'), default=1,primary_key=True)
	product = db.relationship('Product', lazy=False)
	category_id = db.Column(db.Integer(), db.ForeignKey('categories.category_id'), default=1, primary_key=True)
	category = db.relationship('Category', lazy=False)