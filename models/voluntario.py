from models.db import db
from sqlalchemy.sql import func
from models.voluntario_funcao import voluntario_funcao_association

class Voluntario(db.Model):
    __tablename__ = "voluntario"

    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)
    codigo_rfid = db.Column(db.String(50), unique=True)
    data_entrada = db.Column(db.DateTime, default=func.now())
    status = db.Column(db.String(10), default="ativo")

    pessoa = db.relationship('Pessoa', back_populates='voluntario')
    pontos = db.relationship('Ponto', back_populates='voluntario', lazy='dynamic')
    movimentacoes = db.relationship('Movimentacao', back_populates='voluntario', lazy='dynamic')
    funcoes = db.relationship('Funcao', 
                              secondary=voluntario_funcao_association, 
                              back_populates='voluntarios', 
                              lazy='dynamic')
