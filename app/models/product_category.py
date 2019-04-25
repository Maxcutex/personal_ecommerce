from .base_model import BaseModel, db

class ProductCategory(BaseModel):
	__tablename__ = 'product_category'

	product_id = db.Column(db.Integer(),  db.ForeignKey('product.product_id'), default=1,primary_key=True)
	product = db.relationship('Product', lazy=False)
	category_id = db.Column(db.Integer(), db.ForeignKey('category.category_id'), default=1, primary_key=True)
	category = db.relationship('Category', lazy=False)