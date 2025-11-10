# controllers/login_controller.py
from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required
from models.user.usuarios import Usuario

login_bp = Blueprint("login", __name__, template_folder="../views")

@login_bp.route("/login", methods=["GET"])
def index():
    return render_template("login.html")

@login_bp.route("/validated_user", methods=["POST"])
def validated_user():
    login = request.form.get("login")
    senha = request.form.get("password")

    usuario = Usuario.get_single_usuario(login)

    if usuario and usuario.check_password(senha):
        if usuario.status != "ativo":
            flash("Este usuário está inativo.. Entre em contato com o admin.")
            return redirect(url_for("login.index"))

        login_user(usuario)
        return redirect("/home")

    flash("Login ou senha incorretos.", "error")
    return redirect(url_for("login.index"))

@login_bp.route("/logoff")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.index"))
