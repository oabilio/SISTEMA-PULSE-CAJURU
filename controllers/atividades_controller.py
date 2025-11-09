from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.voluntarios.atividade import Atividade
from models.db import db

atividades_bp = Blueprint("atividades", __name__, template_folder="../views")

@atividades_bp.route('/atividades')
def atividades():
    todas_atividades = Atividade.get_atividades()
    return render_template("atividades.html", atividades=todas_atividades)

@atividades_bp.route('/cadastrar_atividade')
def cadastrar_atividade():
    return render_template("cadastrar_atividade.html")

@atividades_bp.route('/add_atividade', methods=['POST'])
def add_atividade():
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    custo_hora = request.form.get("custo_hora") or 0.0

    if Atividade.buscar_atividade(nome):
        flash("Atividade já existe!", "error")
        return redirect(url_for('atividades.cadastrar_atividade'))

    Atividade.save_atividade(nome=nome, descricao=descricao, custo_hora=custo_hora)
    flash("Atividade cadastrada com sucesso!", "success")
    return redirect("/atividades")

@atividades_bp.route('/edit_atividade')
def edit_atividade():
    atividade_id = request.args.get('id')
    atividade = Atividade.query.get(atividade_id)
    return render_template("editar_atividade.html", atividade=atividade)

@atividades_bp.route('/update_atividade', methods=['POST'])
def update_atividade():
    atividade_id = request.form.get('id')
    atividade = Atividade.query.get(atividade_id)
    
    atividade.update_atividade(
        nome=request.form.get('nome'),
        descricao=request.form.get('descricao'),
        custo_hora=request.form.get('custo_hora')
    )

    flash("Atividade atualizada com sucesso!", "success")
    return redirect("/atividades")

@atividades_bp.route('/deletar_atividade', methods=['GET'])
def deletar_atividade():
    atividade_id = request.args.get("id")
    atividade = Atividade.query.get(atividade_id)

    if atividade.voluntarios.count() > 0:
        flash("Precisa remover os voluntários associados antes de deletar a atividade.", "error")
        return redirect("/funcoes")

    db.session.delete(atividade)
    db.session.commit()
    flash("Atividade deletada com sucesso!", "success")
    return redirect("/atividades")
