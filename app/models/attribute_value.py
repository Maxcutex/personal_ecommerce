"""module of attribute value model class"""
from .base_model import BaseModel, db


class AttributeValue(BaseModel):
    """Attribute Value Model class"""
    __tablename__ = 'attribute_values'

    attribute_value_id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(100), nullable=False)
    attribute_id = db.Column(db.Integer(), db.ForeignKey('attributes.attribute_id'), default=1)
    attribute = db.relationship('Attribute', lazy=False)
