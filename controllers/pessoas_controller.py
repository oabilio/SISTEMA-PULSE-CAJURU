# controllers/pessoas_controller.py
from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_login import login_required
from models.user.pessoa import Pessoa
from models.user.endereco import Endereco
from datetime import datetime

pessoas_bp = Blueprint("pessoas", __name__, template_folder="../views")

@pessoas_bp.route('/cadastrar_pessoa')
@login_required
def cadastrar_pessoa():
    next_page = request.args.get('next')
    return render_template("cadastro_pessoa.html", next_page=next_page)

@pessoas_bp.route('/add_pessoa', methods=['POST'])
@login_required
def add_pessoa():
    nome = request.form.get("first_name")
    cpf = request.form.get("cpf")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    data_nasc_str = request.form.get("data_nasc")
    data_nasc_obj = datetime.strptime(data_nasc_str, '%Y-%m-%d').date() if data_nasc_str else None

    Pessoa.save_pessoa(nome=nome, cpf=cpf, telefone=telefone, data_nasc=data_nasc_obj, email=email)

    #flash("Pessoa cadastrada com sucesso!")

    next_page = request.form.get("next_page")
    if next_page:
        return redirect(next_page)
    return redirect("/home")