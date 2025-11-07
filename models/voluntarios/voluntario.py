from models.db import db
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from models.voluntarios.voluntario_atividade import voluntario_atividade_association

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

    def generate_pairing_code(self):
        import random
        code = str(random.randint(1000, 9999))
        self.rfid_pairing_code = code
        self.rfid_pairing_expiry = datetime.now() + timedelta(minutes=5)
        db.session.commit()
        return code

    @staticmethod
    def find_by_pairing_code(code):
        return Voluntario.query.filter(
            Voluntario.rfid_pairing_code == code,
            Voluntario.rfid_pairing_expiry > datetime.now()
        ).first()

    def clear_pairing_code(self):
        self.rfid_pairing_code = None
        self.rfid_pairing_expiry = None
        db.session.commit()