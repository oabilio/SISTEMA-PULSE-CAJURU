from models.db import db
from sqlalchemy.sql import func
from datetime import datetime

class Ponto(db.Model):
    __tablename__ = "ponto"

    id = db.Column(db.Integer, primary_key=True)
    entrada = db.Column(db.DateTime, nullable=False)
    saida = db.Column(db.DateTime, nullable=True)
    origem = db.Column(db.String(100), nullable=True)
    observacao = db.Column(db.Text, nullable=True)
    rfid = db.Column(db.String(100), nullable=True)
    id_voluntario = db.Column(db.Integer, db.ForeignKey("voluntario.id"), nullable=False)

    atividade_id = db.Column(db.Integer, db.ForeignKey("atividade.id"), nullable=True)

    voluntario = db.relationship("Voluntario", backref="pontos")
    atividade = db.relationship("Atividade", backref="pontos")

    @property
    def duracao(self):
        if self.saida and self.entrada:
            return self.saida - self.entrada
        return None

    @staticmethod
    def get_pontos_abertos():
        return (
            Ponto.query.filter(Ponto.saida == None).order_by(Ponto.entrada.desc()).all()
        )

    @staticmethod
    def get_pontos_fechados(limit=100):
        return (
            Ponto.query.filter(Ponto.saida != None)
            .order_by(Ponto.entrada.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_ponto_by_id(ponto_id):
        return Ponto.query.get(ponto_id)

    @staticmethod
    def registrar_batida_rfid(id_voluntario, rfid_tag, origem_batida):
        ponto_aberto = Ponto.query.filter(
            Ponto.id_voluntario == id_voluntario, Ponto.saida == None
        ).first()

        if ponto_aberto:
            ponto_aberto.saida = datetime.now()
            ponto_aberto.observacao = (
                ponto_aberto.observacao or ""
            ) + f"\nSaída por {origem_batida}."
            db.session.commit()
            return "saida"
        else:
            novo_ponto = Ponto(
                id_voluntario=id_voluntario,
                entrada=datetime.now(),
                saida=None,
                origem=origem_batida,
                rfid=rfid_tag,
            )
            db.session.add(novo_ponto)
            db.session.commit()
            return "entrada"
