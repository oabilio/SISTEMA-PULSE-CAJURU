from models.db import db

class Movimentacao(db.Model):
    __tablename__ = "movimentacao"

    id = db.Column(db.Integer, primary_key=True)
    solicitante = db.Column(db.String(100), nullable=False)
    paciente = db.Column(db.String(100), nullable=False)
    id_voluntario = db.Column(db.Integer, db.ForeignKey('voluntario.id'), nullable=False)
    data = db.Column(db.Date, nullable=True)

    origem_id = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)
    destino_id = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)

    voluntario = db.relationship('Voluntario', backref='movimentacoes')

    origem = db.relationship('Setor', foreign_keys=[origem_id], back_populates='movimentacoes_origem')
    destino = db.relationship('Setor', foreign_keys=[destino_id], back_populates='movimentacoes_destino')
