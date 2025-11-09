# models/documentos/doc1.py
from datetime import datetime
from models.db import db

class Doc1(db.Model):
    __tablename__ = "doc1"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=True)
    local_nascimento = db.Column(db.String(100), nullable=True)
    cpf = db.Column(db.String(20), nullable=True)
    estado_civil = db.Column(db.String(50), nullable=True)
    nome_conjuge = db.Column(db.String(100), nullable=True)
    nome_pai = db.Column(db.String(100), nullable=True)
    nome_mae = db.Column(db.String(100), nullable=True)
    endereco_residencial = db.Column(db.String(200), nullable=True)
    numero = db.Column(db.String(20), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    cep = db.Column(db.String(20), nullable=True)
    tel_residencial = db.Column(db.String(30), nullable=True)
    celular = db.Column(db.String(30), nullable=True)
    religiao = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    escolaridade_curso = db.Column(db.String(200), nullable=True)
    local_trabalho = db.Column(db.String(150), nullable=True)
    telefone_trabalho = db.Column(db.String(30), nullable=True)
    ocupacao = db.Column(db.String(50), nullable=True)
    tratamento_saude = db.Column(db.String(30), nullable=True)
    tratamento_saude_para = db.Column(db.String(200), nullable=True)
    transporte = db.Column(db.String(200), nullable=True)
    como_soube_voluntariado = db.Column(db.String(200), nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
