from models.db import db
from sqlalchemy.sql import func

class Ponto(db.Model):
    __tablename__ = "ponto"

    id = db.Column(db.Integer, primary_key=True)
    entrada = db.Column(db.DateTime)
    saida = db.Column(db.DateTime, nullable=True)
    horario = db.Column(db.DateTime, default=func.now())
    tipo = db.Column(db.String(50))
    origem = db.Column(db.String(100))
    observacao = db.Column(db.Text)
    rfid = db.Column(db.String(100))
    manual = db.Column(db.Boolean, default=False)
    id_voluntario = db.Column(db.Integer, db.ForeignKey('voluntario.id'), nullable=False)
    
    voluntario = db.relationship('Voluntario', back_populates='pontos')