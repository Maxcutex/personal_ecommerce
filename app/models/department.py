"""module of Department model class"""
from .base_model import BaseModel, db


class Department(BaseModel):
    """Department Model class"""
    __tablename__ = 'departments'

    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))

    def __str__(self):
        return self.name