"""module of region model class"""
from .base_model import BaseModel, db


class Region(BaseModel):
    """region Model class"""
    __tablename__ = 'region'

    region_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))

    def __str__(self):
        return '<Region: {}>'.format(self.name)