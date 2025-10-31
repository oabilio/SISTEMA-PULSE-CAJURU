# funcao.py
from models.db import db
from models.voluntario_funcao import voluntario_funcao_association

class Funcao(db.Model):
    __tablename__ = "funcao"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    custo_hora = db.Column(db.Numeric(10, 2), default=0.0)
    ativo = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(50))
    
    usuarios = db.relationship('Usuario', back_populates='funcao', lazy='dynamic')
    
    voluntarios = db.relationship('Voluntario', 
                                  secondary=voluntario_funcao_association, 
                                  back_populates='funcoes', 
                                  lazy='dynamic')