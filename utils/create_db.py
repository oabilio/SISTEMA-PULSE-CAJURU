from flask import Flask
from models.db import db
from models.user.roles import Role
from models.user.usuarios import Usuario
from models.user.pessoa import Pessoa

def create_db(app: Flask):
    with app.app_context():
        db.drop_all() 
        db.create_all()

        admin_role = Role.save_role("admin", "Administrador do PULSE")
        comum_role = Role.save_role("comum", "Usuário padrão do PULSE")

        pessoa_admin = Pessoa.save_pessoa(
            nome="Abilio Pedro",
            cpf="123.456.789-11",
            telefone="(41) 99999-9999",
            data_nasc="2000-05-20",
            email="abilio.pedro@hospitaldocajuru.com.br"
        )

        pessoa_user = Pessoa.save_pessoa(
            nome="Samuel Pereira",
            cpf="123.456.789-10",
            telefone="(42) 99999-9999",
            data_nasc="2000-11-04",
            email="samuel.pereira@hospitaldocajuru.com.br"
        )

        Usuario.save_usuario(
            pessoa_id=pessoa_admin.id,
            login="abiliopedro",
            senha="admin123",
            role_id=admin_role.id
        )

        Usuario.save_usuario(
            pessoa_id=pessoa_user.id,
            login="samuelpereira",
            senha="user123",
            role_id=comum_role.id
        )
        
        print("PULSE - Banco criado e populado com usuarios admin e user.")