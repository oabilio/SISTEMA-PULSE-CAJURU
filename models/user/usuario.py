#users.py
from models.db import db
from models.user.roles import Role
from werkzeug.security import generate_password_hash

class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)
    login = db.Column(db.String(100), nullable=False, unique=True)
    senha_hash = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(10), default="ativo")
    tipo = db.Column(db.String(10), default="comum")

    pessoa = db.relationship('Pessoa', back_populates='usuario')