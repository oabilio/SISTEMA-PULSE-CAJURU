from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.voluntarios.setor import Setor
from models.db import db

setores_bp = Blueprint("setores", __name__, template_folder="../views")

@setores_bp.route('/setores')
def setores():
    todos_setores = Setor.get_setores()
    return render_template("setores.html", setores=todos_setores)

@setores_bp.route('/cadastrar_setor')
def cadastrar_setor():
    return render_template("cadastrar_setor.html")

@setores_bp.route('/add_setor', methods=['POST'])
def add_setor():
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")

    if Setor.buscar_setor(nome):
        flash("Setor já existe!", "error")
        return redirect(url_for('setores.cadastrar_setor'))

    Setor.save_setor(nome=nome, descricao=descricao)
    flash("Setor cadastrado com sucesso!", "success")
    return redirect("/setores")

@setores_bp.route('/edit_setor')
def edit_setor():
    setor_id = request.args.get('id')
    setor = Setor.query.get(setor_id)
    return render_template("editar_setor.html", setor=setor)

@setores_bp.route('/update_setor', methods=['POST'])
def update_setor():
    setor_id = request.form.get('id')
    setor = Setor.query.get(setor_id)
    
    setor.update_setor(
        nome=request.form.get('nome'),
        descricao=request.form.get('descricao')
    )

    flash("Setor atualizado com sucesso!", "success")
    return redirect("/setores")

@setores_bp.route('/deletar_setor', methods=['GET'])
def deletar_setor():
    setor_id = request.args.get("id")
    setor = Setor.query.get(setor_id)

    if setor.movimentacoes_origem or setor.movimentacoes_destino:
        flash("Não é possível deletar este setor pois ele está associado a movimentações.", "error")
        return redirect("/setores")

    db.session.delete(setor)
    db.session.commit()
    flash("Setor deletado com sucesso!", "success")
    return redirect("/setores")
