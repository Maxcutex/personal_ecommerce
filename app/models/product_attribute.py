"""module of Product attribute model class"""
from .base_model import BaseModel, db


class ProductAttribute(BaseModel):
    """ Product Attribute Model class"""
    __tablename__ = 'product_attribute'

    product_id = db.Column(db.Integer(), primary_key=True)
    attribute_value_id = db.Column(db.Integer(), primary_key=True)
