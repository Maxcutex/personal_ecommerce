from .base_model import BaseModel, db

class ShippingRegion(BaseModel):
	__tablename__ = 'shipping_region'

	shipping_region = db.Column(db.String(100), nullable=False)