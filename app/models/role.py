"""module of attribute model class"""
from .base_model import BaseModel, db

class Role(BaseModel):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Role: {}>'.format(self.name)