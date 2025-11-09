# controllers/usuarios_controller.py
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required
from models.user.usuarios import Usuario
from models.user.roles import Role
from models.user.pessoa import Pessoa
from models.db import db

usuarios_bp = Blueprint("usuarios", __name__, template_folder="../views")

@usuarios_bp.route("/usuarios")
@login_required
def usuarios():
    usuarios = Usuario.query.all()
    return render_template("usuarios.html", usuarios=usuarios)

@usuarios_bp.route("/cadastrar_usuario", methods=["GET", "POST"])
@login_required
def cadastrar_usuario():
    if request.method == "POST":
        pessoa_id = request.form.get("pessoa_id")
        login = request.form.get("login")
        senha = request.form.get("senha")
        role_id = request.form.get("role_id")

        Usuario.save_usuario(pessoa_id=pessoa_id, login=login, senha=senha, role_id=role_id)
        flash("Usuário cadastrado com sucesso!", "success")
        return redirect("/usuarios")

    pessoas_disponiveis = Pessoa.query.filter(Pessoa.usuario == None).all()
    roles = Role.query.all()
    return render_template("cadastro_usuario.html", pessoas=pessoas_disponiveis, roles=roles)

@usuarios_bp.route("/editar_usuario/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def editar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        flash("Usuário não encontrado.", "error")
        return redirect("/usuarios")

    if request.method == "POST":
        usuario.login = request.form.get("login")
        nova_senha = request.form.get("senha")
        usuario.role_id = request.form.get("role_id")

        if nova_senha:
            from werkzeug.security import generate_password_hash
            usuario.senha_hash = generate_password_hash(nova_senha)

        db.session.commit()
        flash("Usuário atualizado com sucesso!", "success")
        return redirect("/usuarios")

    roles = Role.query.all()
    return render_template("editar_usuario.html", usuario=usuario, roles=roles)

@usuarios_bp.route("/deletar_usuario/<int:usuario_id>")
@login_required
def deletar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        flash("Usuário não encontrado.", "error")
        return redirect("/usuarios")

    if usuario.role.name.lower() == "admin":
        flash("Não é permitido excluir um usuário administrador.", "error")
        return redirect("/usuarios")

    db.session.delete(usuario)
    db.session.commit()
    flash(f"Usuário '{usuario.login}' deletado com sucesso!", "success")
    return redirect("/usuarios")
