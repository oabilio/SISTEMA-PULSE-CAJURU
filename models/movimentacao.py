from models.db import db
from sqlalchemy.sql import func

class Movimentacao(db.Model):
    __tablename__ = "movimentacao"

    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.DateTime, default=func.now())
    origem = db.Column(db.String(100))
    destino = db.Column(db.String(100))   
    id_voluntario = db.Column(db.Integer, db.ForeignKey('voluntario.id'), nullable=False)
    
    voluntario = db.relationship('Voluntario', back_populates='movimentacoes')