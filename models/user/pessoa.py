# pessoa.py
from models.db import db
from sqlalchemy.sql import func

class Pessoa(db.Model):
    __tablename__ = "pessoa"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(14), unique = True, nullable = True)
    telefone = db.Column(db.String(25), nullable = True)
    data_nasc = db.Column(db.Date, nullable = True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    criado_em = db.Column(db.DateTime(timezone = True), server_default = func.now())

    usuario = db.relationship('usuario', back_populates = 'pessoa', uselist=False)
    voluntario = db.relationship('voluntario', back_populates='pessoa', uselist=False)
    enderecos = db.relationship('endereco', back_populates = 'pessoa', lazy = 'dynamic', cascade = 'all, delete-orphan')
