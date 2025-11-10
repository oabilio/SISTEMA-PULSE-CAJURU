# models/documentos/doc3.py
from datetime import datetime
from models.db import db

class Doc3(db.Model):
    __tablename__ = "doc3"

    id = db.Column(db.Integer, primary_key=True)

    segunda_inicio = db.Column(db.String(20), nullable=True)
    segunda_fim  = db.Column(db.String(20), nullable=True)
    terca_inicio  = db.Column(db.String(20), nullable=True)
    terca_fim  = db.Column(db.String(20), nullable=True)
    quarta_inicio = db.Column(db.String(20), nullable=True)
    quarta_fim = db.Column(db.String(20), nullable=True)
    quinta_inicio = db.Column(db.String(20), nullable=True)
    quinta_fim = db.Column(db.String(20), nullable=True)
    sexta_inicio = db.Column(db.String(20), nullable=True)
    sexta_fim = db.Column(db.String(20), nullable=True)
    sabado_inicio = db.Column(db.String(20), nullable=True)
    sabado_fim = db.Column(db.String(20), nullable=True)
    domingo_inicio = db.Column(db.String(20), nullable=True)
    domingo_fim = db.Column(db.String(20), nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)