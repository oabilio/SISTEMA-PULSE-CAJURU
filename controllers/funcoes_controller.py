from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.voluntarios.funcao import Funcao
from models.db import db

funcoes_bp = Blueprint("funcoes", __name__, template_folder="../views")

@funcoes_bp.route('/funcoes')
def funcoes():
    todas_funcoes = Funcao.get_funcoes()
    return render_template("funcoes.html", funcoes=todas_funcoes)

@funcoes_bp.route('/cadastrar_funcao')
def cadastrar_funcao():
    return render_template("cadastrar_funcao.html")

@funcoes_bp.route('/add_funcao', methods=['POST'])
def add_funcao():
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    custo_hora = request.form.get("custo_hora") or 0.0

    if Funcao.buscar_funcao(nome):
        flash("Função já existe!")
        return redirect(url_for('funcoes.cadastrar_funcao'))

    Funcao.save_funcao(nome=nome, descricao=descricao, custo_hora=custo_hora)
    flash("Função cadastrada com sucesso!")
    return redirect("/funcoes")

@funcoes_bp.route('/edit_funcao')
def edit_funcao():
    funcao_id = request.args.get('id')
    funcao = Funcao.query.get(funcao_id)
    return render_template("update_funcao.html", funcao=funcao)

@funcoes_bp.route('/update_funcao', methods=['POST'])
def update_funcao():
    funcao_id = request.form.get('id')
    funcao = Funcao.query.get(funcao_id)
    
    funcao.update_funcao(
        nome=request.form.get('nome'),
        descricao=request.form.get('descricao'),
        custo_hora=request.form.get('custo_hora')
    )

    flash("Função atualizada com sucesso!")
    return redirect("/funcoes")

@funcoes_bp.route('/deletar_funcao', methods=['GET'])
def deletar_funcao():
    funcao_id = request.args.get("id")
    funcao = Funcao.query.get(funcao_id)

    if funcao.voluntarios.count() > 0:
        flash("Precisa remover os voluntários associados antes de deletar a função.")
        return redirect("/funcoes")

    db.session.delete(funcao)
    db.session.commit()
    flash("Função deletada com sucesso!")
    return redirect("/funcoes")
