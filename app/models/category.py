"""module of attribute model class"""
from .base_model import BaseModel, db


class Category(BaseModel):
    """attribute Model class"""
    __tablename__ = 'categories'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    department_id = db.Column(db.Integer(), db.ForeignKey('departments.id'), default=1)
    department = db.relationship('Department', lazy=False)


    def __str__(self):
        return self.name
