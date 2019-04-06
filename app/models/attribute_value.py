"""module of attribute value model class"""
from .base_model import BaseModel, db


class AttributeValue(BaseModel):
    """Attribute Value Model class"""
    __tablename__ = 'attribute_values'

    value = db.Column(db.String(100))
    attribute_id = db.Column(db.Integer(), db.ForeignKey('attributes.id'), default=1)
    attribute = db.relationship('Attribute', lazy=False)
