# models/documentos/pendencia.py
import uuid
from datetime import datetime
from sqlalchemy.dialects.mysql import JSON
from models.db import db

class Pendencia(db.Model):
    __tablename__ = "pendencias"

    id = db.Column(db.Integer, primary_key=True)
    documentacao_id = db.Column(db.Integer, db.ForeignKey("documentacao.id"), nullable=False)
    uuid_link = db.Column(db.String(36), unique=True, nullable=True, default=lambda: str(uuid.uuid4()))
    status = db.Column(db.String(20), nullable=False, default="gerado")  
    payload = db.Column(JSON, nullable=True)
    nome_candidato = db.Column(db.String(255), nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    documentacao = db.relationship("Documentacao", backref=db.backref("pendencias", lazy=True))
