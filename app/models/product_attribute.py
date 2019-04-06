"""module of Product attribute model class"""
from .base_model import BaseModel, db


class ProductAttribute(BaseModel):
    """ Product Attribute Model class"""
    __tablename__ = 'product_attributes'

    product_id = db.Column(db.Integer())
    attribute_value_id = db.Column(db.Integer(), db.ForeignKey('attribute_values.id'), default=1)
    attribute_value = db.relationship('AttributeValue', lazy=False)
