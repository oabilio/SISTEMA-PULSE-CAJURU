# models/documentos/documentacao.py
from datetime import datetime
from models.db import db

class Documentacao(db.Model):
    __tablename__ = "documentacao"

    id = db.Column(db.Integer, primary_key=True)
    voluntario_id = db.Column(db.Integer, db.ForeignKey("voluntario.id"), nullable=True)
    
    doc1_id = db.Column(db.Integer, db.ForeignKey("doc1.id"), nullable=True)
    doc2_id = db.Column(db.Integer, db.ForeignKey("doc2.id"), nullable=True)
    doc3_id = db.Column(db.Integer, db.ForeignKey("doc3.id"), nullable=True)
    doc4_id = db.Column(db.Integer, db.ForeignKey("doc4.id"), nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    voluntario = db.relationship("Voluntario", backref=db.backref("documentacoes", lazy=True))
    doc1 = db.relationship("Doc1", backref=db.backref("documentacao", lazy=True))
    doc2 = db.relationship("Doc2", backref=db.backref("documentacao", lazy=True))
    doc3 = db.relationship("Doc3", backref=db.backref("documentacao", lazy=True))
    doc4 = db.relationship("Doc4", backref=db.backref("documentacao", lazy=True))
