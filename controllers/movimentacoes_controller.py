from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.voluntarios.movimentacao import Movimentacao
from models.voluntarios.voluntario import Voluntario
from models.voluntarios.setor import Setor
from models.db import db

movimentacoes_bp = Blueprint("movimentacoes", __name__, template_folder="../views")

@movimentacoes_bp.route('/movimentacoes')
def movimentacoes():
    todas_movimentacoes = Movimentacao.query.all()
    return render_template("movimentacoes.html", movimentacoes=todas_movimentacoes)

@movimentacoes_bp.route('/cadastrar_movimentacao')
def cadastrar_movimentacao():
    voluntarios = Voluntario.query.all()
    setores = Setor.query.all()
    return render_template("cadastrar_movimentacao.html", voluntarios=voluntarios, setores=setores)

@movimentacoes_bp.route('/add_movimentacao', methods=['POST'])
def add_movimentacao():
    solicitante = request.form.get("solicitante")
    paciente = request.form.get("paciente")
    id_voluntario = request.form.get("id_voluntario")
    origem_id = request.form.get("origem_id")
    destino_id = request.form.get("destino_id")
    data = request.form.get("date")

    nova_movimentacao = Movimentacao(
        solicitante=solicitante,
        paciente=paciente,
        id_voluntario=id_voluntario,
        origem_id=origem_id,
        destino_id=destino_id,
        data=data
    )

    db.session.add(nova_movimentacao)
    db.session.commit()

    flash("Movimentação registrada com sucesso!", "success")
    return redirect("/movimentacoes")

@movimentacoes_bp.route('/editar_movimentacao')
def editar_movimentacao():
    mov_id = request.args.get('id')
    movimentacao = Movimentacao.query.get(mov_id)
    voluntarios = Voluntario.query.all()
    setores = Setor.query.all()
    return render_template("editar_movimentacao.html", movimentacao=movimentacao, voluntarios=voluntarios, setores=setores)

@movimentacoes_bp.route('/update_movimentacao', methods=['POST'])
def update_movimentacao():
    mov_id = request.form.get('id')
    movimentacao = Movimentacao.query.get(mov_id)

    movimentacao.solicitante = request.form.get("solicitante")
    movimentacao.paciente = request.form.get("paciente")
    movimentacao.id_voluntario = request.form.get("id_voluntario")
    movimentacao.origem_id = request.form.get("origem_id")
    movimentacao.destino_id = request.form.get("destino_id")
    movimentacao.data = request.form.get("data")

    db.session.commit()
    flash("Movimentação atualizada com sucesso!", "success")
    return redirect("/movimentacoes")

@movimentacoes_bp.route('/deletar_movimentacao', methods=['GET'])
def deletar_movimentacao():
    mov_id = request.args.get("id")
    movimentacao = Movimentacao.query.get(mov_id)

    db.session.delete(movimentacao)
    db.session.commit()
    flash("Movimentação excluída com sucesso!", "success")
    return redirect("/movimentacoes")
