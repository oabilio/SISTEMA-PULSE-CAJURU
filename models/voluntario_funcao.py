from models.db import db

voluntario_funcao_association = db.Table('voluntario_funcao',
    db.Column('id_voluntario', db.Integer, db.ForeignKey('voluntario.id'), primary_key=True),
    db.Column('id_funcao', db.Integer, db.ForeignKey('funcao.id'), primary_key=True)
)