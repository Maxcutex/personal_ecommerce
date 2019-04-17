"""module of attribute model class"""
from .base_model import BaseModel, db


class Attribute(BaseModel):
    """attribute Model class"""
    __tablename__ = 'attributes'

    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.name