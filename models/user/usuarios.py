# models/user/usuarios.py
from models.db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)
    login = db.Column(db.String(100), nullable=False, unique=True)
    senha_hash = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(10), default="ativo")
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role', backref='users', lazy=True)

    @property
    def role_name(self):
        user_role = self.role
        if user_role:
            return user_role.name
        else:
            return "Default"

    @classmethod
    def save_usuario(cls, pessoa_id, login, senha, role_id): 
        hashed_senha = generate_password_hash(senha)
        usuario = cls(
            pessoa_id=pessoa_id, 
            login=login, 
            senha_hash=hashed_senha, 
            role_id=role_id
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)

    @staticmethod
    def get_single_usuario(login):
        return Usuario.query.filter_by(login=login).first()

    @staticmethod
    def get_usuarios():
        return Usuario.query.all()
    
    def has_role(self, role_name):
        return self.role_name == role_name