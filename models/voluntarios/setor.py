from models.db import db
from sqlalchemy.sql import func

class Setor(db.Model):
    __tablename__ = "setor"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime(timezone=True), server_default=func.now())

    movimentacoes_origem = db.relationship(
        'Movimentacao',
        foreign_keys='Movimentacao.origem_id',
        back_populates='origem'
    )

    movimentacoes_destino = db.relationship(
        'Movimentacao',
        foreign_keys='Movimentacao.destino_id',
        back_populates='destino'
    )

    @classmethod
    def save_setor(cls, nome, descricao=None):
        setor = cls(nome=nome, descricao=descricao)
        db.session.add(setor)
        db.session.commit()
        return setor

    @staticmethod
    def buscar_setor(nome):
        return Setor.query.filter_by(nome=nome).first()

    @staticmethod
    def get_setores():
        return Setor.query.all()
    
    def update_setor(self, nome=None, descricao=None):
        if nome is not None:
            self.nome = nome
        if descricao is not None:
            self.descricao = descricao
        db.session.commit()
