# endereco.py
from models.db import db
from datetime import date

class Endereco(db.Model):
    __tablename__ = "endereco"

    id = db.Column(db.Integer, primary_key = True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable = False)
    logradouro = db.Column(db.String(100), nullable = False)
    numero = db.Column(db.String(10), nullable = True)
    bairro = db.Column(db.String(50), nullable = True)
    cidade = db.Column(db.String(50), nullable = False)
    estado = db.Column(db.String(2), nullable = False)
    cep = db.Column(db.String(20), nullable = True)
    complemento = db.Column(db.String(100), nullable = True)

    def save_endereco(pessoa_id, logradouro, numero, bairro, cidade, estado, cep, complemento):
        endereco = Endereco(pessoa_id=pessoa_id,
                            logradouro=logradouro,
                            numero=numero,
                            bairro=bairro,
                            cidade=cidade,
                            estado=estado,
                            cep=cep,
                            complemento=complemento)
        
        db.session.add(endereco)
        db.session.commit()
        return endereco