# models/user/roles.py
from models.db import db

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(512), nullable=True)

    @classmethod
    def save_role(cls, name, description=None):
        role = cls(name=name, description=description)
        db.session.add(role)
        db.session.commit()
        return role

    @staticmethod
    def get_single_role(name):
        return Role.query.filter_by(name=name).first()

    @staticmethod
    def get_roles():
        return Role.query.all()
