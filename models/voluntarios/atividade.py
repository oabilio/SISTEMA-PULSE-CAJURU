# models/voluntarios/atividade.py
from models.db import db
from models.voluntarios.voluntario_atividade import voluntario_atividade_association

class Atividade(db.Model):
    __tablename__ = "atividade"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    custo_hora = db.Column(db.Numeric(10, 2), default=0.0)
    ativo = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(50))
    
    voluntarios = db.relationship('Voluntario', 
                                  secondary=voluntario_atividade_association, 
                                  backref='atividades', 
                                  lazy='dynamic')

    @classmethod
    def save_atividade(cls, nome, descricao=None, custo_hora=0.0, ativo=True, status=None):
        atividade = cls(nome=nome, descricao=descricao, custo_hora=custo_hora, ativo=ativo, status=status)
        db.session.add(atividade)
        db.session.commit()
        return atividade

    @staticmethod
    def buscar_atividade(nome):
        return Atividade.query.filter_by(nome=nome).first()

    @staticmethod
    def get_atividades():
        return Atividade.query.all()
    
    def update_atividade(self, nome=None, descricao=None, custo_hora=None, ativo=None, status=None):
        if nome is not None:
            self.nome = nome
        if descricao is not None:
            self.descricao = descricao
        if custo_hora is not None:
            self.custo_hora = custo_hora
        if ativo is not None:
            self.ativo = ativo
        if status is not None:
            self.status = status

        db.session.commit()
