"""module of attribute value model class"""
from .base_model import BaseModel, db


class AttributeValue(BaseModel):
    """Attribute Value Model class"""
    __tablename__ = 'attribute_value'

    attribute_value_id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(100), nullable=False)
    attribute_id = db.Column(db.Integer(), db.ForeignKey('attribute.attribute_id'), default=1)
    attribute = db.relationship('Attribute', lazy=False)
