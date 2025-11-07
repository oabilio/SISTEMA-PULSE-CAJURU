# models/registro_atividade.py
from models.db import db
from sqlalchemy.sql import func

class RegistroAtividade(db.Model):
    __tablename__ = "registro_atividade"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime(timezone=True), server_default=func.now())

    ponto_id = db.Column(db.Integer, db.ForeignKey('ponto.id'), nullable=False)
    funcao_id = db.Column(db.Integer, db.ForeignKey('funcao.id'), nullable=False)

    ponto = db.relationship('Ponto', backref='registro_atividade', lazy=True)
    funcao = db.relationship('Funcao', backref='registro_atividade', lazy=True)
