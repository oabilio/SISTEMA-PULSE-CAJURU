# controllers/documentacoes_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.db import db
from models.documentos.documentacao import Documentacao
from models.documentos.pendencia import Pendencia
from models.voluntarios.voluntario import Voluntario
from datetime import datetime
import uuid

documentacoes_bp = Blueprint("documentacoes", __name__, template_folder="../views")

@documentacoes_bp.route("/documentacoes")
@login_required
def lista_documentacoes():
    voluntarios = Voluntario.query.all()

    dados = []
    for voluntario in voluntarios:
        documentacao = Documentacao.query.filter_by(voluntario_id=voluntario.id).first()
        if documentacao:
            status = "Com documentação"
            acao = {
                "tipo": "info",
                "url": url_for("documentacoes.ver_detalhes", documentacao_id=documentacao.id)
            }
        else:
            status = "Sem documentação"
            acao = {
                "tipo": "criar",
                "url": url_for("documentacoes.criar_para_voluntario", voluntario_id=voluntario.id)
            }

        dados.append({
            "voluntario": voluntario,
            "documentacao": documentacao,
            "status": status,
            "acao": acao
        })

    return render_template("documentacoes.html", dados=dados)

@documentacoes_bp.route("/documentacoes/criar/<int:voluntario_id>")
@login_required
def criar_para_voluntario(voluntario_id):
    voluntario = Voluntario.query.get_or_404(voluntario_id)

    nova_doc = Documentacao(voluntario_id=voluntario.id)
    db.session.add(nova_doc)
    db.session.commit()

    flash(f"Documentação criada para {voluntario.pessoa.nome}.", "success")
    return redirect(url_for("documentacoes.lista_documentacoes"))

# @documentacoes_bp.route("/documentacoes/criar_nova")
# @login_required
# def criar_nova():
#     return redirect(url_for("documentacoes.lista_documentacoes"))

@documentacoes_bp.route("/documentacoes/<int:documentacao_id>")
@login_required
def ver_detalhes(documentacao_id):
    doc = Documentacao.query.get_or_404(documentacao_id)
    return render_template("documentacoes/detalhes_documentacao.html", doc=doc)

@documentacoes_bp.route("/documentacao/preencher/<uuid>", methods=["GET", "POST"])
def preencher(uuid):
    pendencia = Pendencia.query.filter_by(uuid_link=uuid).first_or_404()
    documentacao = pendencia.documentacao

    if request.method == "GET":
        return render_template("formulario_publico.html", documentacao=documentacao, pendencia=pendencia)

    data = request.get_json() if request.is_json else request.form.to_dict()

    pendencia.payload = data

    nome = data.get("nome")
    if nome:
        pendencia.nome_candidato = nome

    pendencia.status = "preenchido"
    pendencia.atualizado_em = datetime.utcnow()

    pendencia.uuid_link = None

    db.session.commit()
    flash("Formulário preenchido com sucesso!", "success")
    return redirect(url_for("documentacoes.confirmacao"))

@documentacoes_bp.route("/documentacao/confirmacao")
def confirmacao():
    return render_template("confirmacao.html")