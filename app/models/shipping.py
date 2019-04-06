"""module of shipping model class"""
from .base_model import BaseModel, db


class Shipping(BaseModel):
    """attribute Model class"""
    __tablename__ = 'shipping'

    name = db.Column(db.String(100))
    type = db.Column(db.String(400))
    cost = db.Column(db.String(100))
    region_id = db.Column(db.Integer(), db.ForeignKey('regions.id'), default=1)
    region = db.relationship('Region', lazy=False)

    def __str__(self):
        return self.name