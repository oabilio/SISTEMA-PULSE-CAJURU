# models/user/pessoa.py
from models.db import db
from sqlalchemy.sql import func
from sqlalchemy import Date 

class Pessoa(db.Model):
    __tablename__ = "pessoa"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(14), unique = True, nullable = True)
    telefone = db.Column(db.String(25), nullable = True)
    data_nasc = db.Column(Date, nullable = True) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    criado_em = db.Column(db.DateTime(timezone = True), server_default = func.now())

    usuario = db.relationship('Usuario', backref='pessoa', uselist=False)
    voluntario = db.relationship('Voluntario', backref='pessoa', uselist=False)
    endereco = db.relationship('Endereco', backref = 'pessoa', cascade = 'all, delete-orphan')

    @classmethod
    def save_pessoa(cls, nome, cpf, telefone, data_nasc, email):
        pessoa = cls(nome=nome,
                        cpf=cpf,
                        telefone=telefone,
                        data_nasc=data_nasc,
                        email=email)
        db.session.add(pessoa)
        db.session.commit()
        return pessoa