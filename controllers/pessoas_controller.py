# controllers/pessoas_controller.py
from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_login import login_required
from models.user.pessoa import Pessoa
from datetime import datetime
from models import db

pessoas_bp = Blueprint("pessoas", __name__, template_folder="../views")

@pessoas_bp.route('/pessoas')
@login_required
def pessoas():
    todas_pessoas = Pessoa.query.all()
    return render_template("pessoas.html", pessoas=todas_pessoas)

@pessoas_bp.route('/cadastrar_pessoa')
@login_required
def cadastrar_pessoa():
    next_page = request.args.get('next')
    return render_template("cadastro_pessoa.html", next_page=next_page)

@pessoas_bp.route('/add_pessoa', methods=['POST'])
@login_required
def add_pessoa():
    nome = request.form.get("name")
    cpf = request.form.get("cpf")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    data_nasc_str = request.form.get("data_nasc")
    data_nasc_obj = datetime.strptime(data_nasc_str, '%Y-%m-%d').date() if data_nasc_str else None

    if Pessoa.query.filter((Pessoa.cpf == cpf) | (Pessoa.email == email)).first():
        flash("Pessoa com CPF ou e-mail já cadastrado!", "error")
        return redirect(url_for('pessoas.cadastrar_pessoa'))

    Pessoa.save_pessoa(nome=nome, cpf=cpf, telefone=telefone, data_nasc=data_nasc_obj, email=email)
    flash("Pessoa cadastrada com sucesso!", "success")

    next_page = request.form.get("next_page")
    if next_page:
        return redirect(next_page)
    return redirect(url_for('pessoas.pessoas'))

@pessoas_bp.route('/editar_pessoa')
@login_required
def editar_pessoa():
    pessoa_id = request.args.get('id')
    pessoa = Pessoa.query.get(pessoa_id)
    if not pessoa:
        flash("Pessoa não encontrada.", "error")
        return redirect(url_for('pessoas_bp.pessoas'))
    return render_template("editar_pessoa.html", pessoa=pessoa)

@pessoas_bp.route('/update_pessoa', methods=['POST'])
@login_required
def update_pessoa():
    pessoa_id = request.form.get('id')
    pessoa = Pessoa.query.get(pessoa_id)
    if not pessoa:
        flash("Pessoa não encontrada.", "error")
        return redirect(url_for('pessoas.pessoas'))

    nome = request.form.get("name")
    cpf = request.form.get("cpf")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    data_nasc_str = request.form.get("data_nasc")
    data_nasc_obj = datetime.strptime(data_nasc_str, '%Y-%m-%d').date() if data_nasc_str else None

    pessoa.nome = nome
    pessoa.cpf = cpf
    pessoa.telefone = telefone
    pessoa.email = email
    pessoa.data_nasc = data_nasc_obj

    db.session.commit()

    flash("Pessoa atualizada com sucesso!", "success")
    return redirect(url_for('pessoas.pessoas'))

@pessoas_bp.route('/deletar_pessoa')
@login_required
def deletar_pessoa():
    pessoa_id = request.args.get("id")
    pessoa = Pessoa.query.get(pessoa_id)
    if not pessoa:
        flash("Pessoa não encontrada.", "error")
        return redirect(url_for('pessoas.pessoas'))

    db.session.delete(pessoa)
    db.session.commit()

    flash("Pessoa deletada com sucesso!", "success")
    return redirect(url_for('pessoas.pessoas'))

@pessoas_bp.route('/info_pessoa')
@login_required
def info_pessoa():
    pessoa_id = request.args.get("id")
    pessoa = Pessoa.query.get(pessoa_id)
    if not pessoa:
        flash("Pessoa não encontrada.", "error")
        return redirect(url_for('pessoas.pessoas'))

    return render_template("info_pessoa.html", pessoa=pessoa)