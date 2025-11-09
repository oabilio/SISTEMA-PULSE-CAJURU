# models/documentos/doc2.py
from datetime import datetime
from models.db import db

class Doc2(db.Model):
    __tablename__ = "doc2"

    id = db.Column(db.Integer, primary_key=True)

    ja_trabalhou_voluntario = db.Column(db.String(20), nullable=True)
    ja_trabalhou_voluntario_onde = db.Column(db.String(200), nullable=True)

    faz_parte_grupo_voluntariado = db.Column(db.String(20), nullable=True)
    qual_grupo_voluntariado = db.Column(db.String(200), nullable=True)

    contribuicao_voluntariado = db.Column(db.Text, nullable=True)

    habilidade_musical = db.Column(db.String(20), nullable=True)
    qual_habilidade_musical = db.Column(db.String(200), nullable=True)

    auxiliar_alimentacao = db.Column(db.String(20), nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
