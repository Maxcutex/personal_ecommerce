"""module of attribute model class"""
from .base_model import BaseModel, db


class Category(BaseModel):
    """attribute Model class"""
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    department_id = db.Column(db.Integer(), db.ForeignKey('departments.department_id'), default=1)
    department = db.relationship('Department', lazy=False)


    def __str__(self):
        return self.name
