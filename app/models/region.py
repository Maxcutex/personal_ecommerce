"""module of region model class"""
from .base_model import BaseModel, db


class Region(BaseModel):
    """region Model class"""
    __tablename__ = 'regions'

    name = db.Column(db.String(100))

    def __str__(self):
        return self.name