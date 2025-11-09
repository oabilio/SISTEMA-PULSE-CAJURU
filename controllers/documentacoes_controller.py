# controllers/documentacoes_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.db import db
from models.documentos.documentacao import Documentacao
from models.documentos.pendencia import Pendencia
from models.voluntarios.voluntario import Voluntario
from models.documentos.doc1 import Doc1
from models.documentos.doc2 import Doc2
from models.documentos.doc3 import Doc3
from models.documentos.doc4 import Doc4
from models.documentos.documentacao import Documentacao
from datetime import datetime

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

@documentacoes_bp.route("/documentacoes/criar_manual/<int:voluntario_id>", methods=["GET", "POST"])
@login_required
def criar_manual(voluntario_id):
    voluntario = Voluntario.query.get_or_404(voluntario_id)

    if request.method == "GET":
        return render_template("formulario_privado.html", documentacao=None, voluntario=voluntario, modo_manual=True)

    data = dict(request.form)

    date_fields = [
        "data_inicio", "data_acolher", "data_cav",
        "vacina_inicio", "vacina_final", "foto_data", "cracha_data"
    ]

    for f in date_fields:
        val = data.get(f)
        if val and val != "":
            try:
                data[f] = datetime.strptime(val, "%Y-%m-%d").date()
            except ValueError:
                data[f] = None
        else:
            data[f] = None

    doc1 = Doc1(
        nome=data.get("nome"),
        data_nascimento=data.get("data_nascimento"),
        local_nascimento=data.get("local_nascimento"),
        cpf=data.get("cpf"),
        email=data.get("email"),
        estado_civil=data.get("estado_civil"),
        nome_conjuge=data.get("nome_conjuge"),
        nome_pai=data.get("nome_pai"),
        nome_mae=data.get("nome_mae"),
        endereco_residencial=data.get("endereco_residencial"),
        numero=data.get("numero"),
        bairro=data.get("bairro"),
        cidade=data.get("cidade"),
        cep=data.get("cep"),
        tel_residencial=data.get("tel_residencial"),
        celular=data.get("celular"),
        religiao=data.get("religiao"),
        escolaridade_curso=data.get("escolaridade_curso"),
        local_trabalho=data.get("local_trabalho"),
        telefone_trabalho=data.get("telefone_trabalho"),
        ocupacao=data.get("ocupacao") or data.get("ocupacao_outro_texto"),
        tratamento_saude=data.get("tratamento_saude"),
        tratamento_saude_para=data.get("tratamento_saude_para"),
        transporte=data.get("transporte"),
        como_soube_voluntariado=data.get("como_soube_voluntariado"),
    )

    doc2 = Doc2(
        ja_trabalhou_voluntario=data.get("ja_trabalhou_voluntario"),
        ja_trabalhou_voluntario_onde=data.get("ja_trabalhou_voluntario_onde"),
        faz_parte_grupo_voluntariado=data.get("faz_parte_grupo_voluntariado"),
        qual_grupo_voluntariado=data.get("qual_grupo_voluntariado"),
        contribuicao_voluntariado=data.get("contribuicao_voluntariado"),
        habilidade_musical=data.get("habilidade_musical"),
        qual_habilidade_musical=data.get("qual_habilidade_musical"),
        auxiliar_alimentacao=data.get("auxiliar_alimentacao"),
    )

    doc3 = Doc3(
        segunda_inicio=data.get("segunda_inicio"),
        segunda_fim=data.get("segunda_fim"),
        terca_inicio=data.get("terca_inicio"),
        terca_fim=data.get("terca_fim"),
        quarta_inicio=data.get("quarta_inicio"),
        quarta_fim=data.get("quarta_fim"),
        quinta_inicio=data.get("quinta_inicio"),
        quinta_fim=data.get("quinta_fim"),
        sexta_inicio=data.get("sexta_inicio"),
        sexta_fim=data.get("sexta_fim"),
        sabado_inicio=data.get("sabado_inicio"),
        sabado_fim=data.get("sabado_fim"),
        domingo_inicio=data.get("domingo_inicio"),
        domingo_fim=data.get("domingo_fim"),
    )

    doc4 = Doc4(
        aprovado=data.get("aprovado"),
        motivo=data.get("motivo"),
        data_inicio=data.get("data_inicio"),
        data_acolher=data.get("data_acolher"),
        data_cav=data.get("data_cav"),
        vacina_inicio=data.get("vacina_inicio"),
        vacina_final=data.get("vacina_final"),
        foto_data=data.get("foto_data"),
        cracha_data=data.get("cracha_data"),
    )

    db.session.add_all([doc1, doc2, doc3, doc4])
    db.session.commit()

    documentacao = Documentacao(
        voluntario_id=voluntario.id,
        doc1_id=doc1.id,
        doc2_id=doc2.id,
        doc3_id=doc3.id,
        doc4_id=doc4.id,
    )

    db.session.add(documentacao)
    db.session.commit()

    flash(f"Documentação criada para {voluntario.pessoa.nome}.", "success")
    return redirect(url_for("documentacoes.lista_documentacoes"))

@documentacoes_bp.route("/documentacoes/<int:documentacao_id>")
@login_required
def ver_detalhes(documentacao_id):
    doc = Documentacao.query.get_or_404(documentacao_id)
    return render_template("documentacoes/detalhes_documentacao.html", doc=doc)

@documentacoes_bp.route("/documentacoes/info/<int:voluntario_id>")
@login_required
def info_voluntario(voluntario_id):
    voluntario = Voluntario.query.get_or_404(voluntario_id)
    pessoa = voluntario.pessoa

    documentacao = getattr(voluntario, "documentacao", None)

    doc1 = documentacao.doc1 if documentacao and documentacao.doc1 else None
    doc2 = documentacao.doc2 if documentacao and documentacao.doc2 else None
    doc3 = documentacao.doc3 if documentacao and documentacao.doc3 else None
    doc4 = documentacao.doc4 if documentacao and documentacao.doc4 else None

    return render_template("info_voluntario.html", voluntario=voluntario, pessoa=pessoa, doc1=doc1, doc2=doc2, doc3=doc3, doc4=doc4)

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
    return redirect(url_for("documentacoes.confirmacao"))

@documentacoes_bp.route("/documentacao/confirmacao")
def confirmacao():
    return render_template("confirmacao.html")