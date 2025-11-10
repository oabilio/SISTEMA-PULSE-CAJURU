# models/documentos/doc4.py
from datetime import datetime
from models.db import db

class Doc4(db.Model):
    __tablename__ = "doc4"

    id = db.Column(db.Integer, primary_key=True)

    aprovado = db.Column(db.String(10), nullable=True)
    motivo = db.Column(db.Text, nullable=True)

    data_inicio = db.Column(db.Date, nullable=True)
    data_acolher = db.Column(db.Date, nullable=True)
    data_cav = db.Column(db.Date, nullable=True)

    vacina_inicio = db.Column(db.Date, nullable=True)
    vacina_final = db.Column(db.Date, nullable=True)

    foto_data = db.Column(db.Date, nullable=True)
    cracha_data = db.Column(db.Date, nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
