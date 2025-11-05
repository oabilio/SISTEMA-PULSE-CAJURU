# voluntario.py
from models.db import db
from sqlalchemy.sql import func
from models.voluntarios.voluntario_funcao import voluntario_funcao_association

class Voluntario(db.Model):
    __tablename__ = "voluntario"

    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)
    codigo_rfid = db.Column(db.String(50), unique=True)
    data_entrada = db.Column(db.DateTime, default=func.now())
    status = db.Column(db.String(10), default="ativo")

    @classmethod
    def save_voluntario(cls, pessoa_id, codigo_rfid=None, status="ativo"):
        voluntario = cls(pessoa_id=pessoa_id, codigo_rfid=codigo_rfid, status=status)
        db.session.add(voluntario)
        db.session.commit()
        return voluntario
