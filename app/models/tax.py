from .base_model import BaseModel, db

class Tax(BaseModel):
	__tablename__ = 'tax'

	tax_type = db.Column(db.String(100), nullable=False)
	tax_percentage = db.Column(db.Float(), nullable=False)
	