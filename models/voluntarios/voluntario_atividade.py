# models/voluntarios/voluntario_atividade.py
from models.db import db

voluntario_atividade_association = db.Table('voluntario_atividade',
    db.Column('id_voluntario', db.Integer, db.ForeignKey('voluntario.id'), primary_key=True),
    db.Column('id_atividade', db.Integer, db.ForeignKey('atividade.id'), primary_key=True)
)