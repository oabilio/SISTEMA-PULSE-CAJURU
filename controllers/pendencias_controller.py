# controllers/pendencias_controller.py
from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_required
from models.db import db
from models.documentos.pendencia import Pendencia
from models.documentos.documentacao import Documentacao
from models.user.pessoa import Pessoa
from models.voluntarios.voluntario import Voluntario
from models.documentos.doc1 import Doc1
from models.documentos.doc2 import Doc2
from models.documentos.doc3 import Doc3
from models.documentos.doc4 import Doc4
from datetime import datetime

pendencias_bp = Blueprint("pendencias", __name__, template_folder="../views")

@pendencias_bp.route("/pendentes")
@login_required
def lista_pendencias():
    pendencias = Pendencia.query.order_by(Pendencia.criado_em.desc()).all()
    return render_template("pendentes.html", pendencias=pendencias)

@pendencias_bp.route("/pendentes/gerar_link", methods=["POST"])
@login_required
def gerar_link():

    nova_doc = Documentacao()
    db.session.add(nova_doc)
    db.session.commit()

    pendencia = Pendencia(documentacao_id=nova_doc.id)
    db.session.add(pendencia)
    db.session.commit()

    flash(f"Link público gerado com sucesso!", "success")
    return redirect(url_for("pendencias.lista_pendencias"))

@pendencias_bp.route("/pendentes/<int:pendencia_id>/avaliar", methods=["GET", "POST"])
@login_required
def avaliar_pendencia(pendencia_id):
    pendencia = Pendencia.query.get_or_404(pendencia_id)
    data = pendencia.payload or {}

    if request.method == "POST":
        form_data = dict(request.form)
        aprovado = form_data.pop("aprovado", None) == "sim"
        motivo = form_data.pop("motivo", None)

        form_data = {
            k: (True if v == "on" else False if v in ("", None, "off") else v)
            for k, v in form_data.items()
        }

        date_fields = [
        "data_inicio", "data_acolher", "data_cav",
        "vacina_inicio", "vacina_final", "foto_data", "cracha_data"
        ]

        for f in date_fields:
            val = form_data.get(f)
            if val and val != "":
                try:
                    form_data[f] = datetime.strptime(val, "%Y-%m-%d").date()
                except ValueError:
                    form_data[f] = None
            else:
                form_data[f] = None

        if not aprovado:
            pendencia.payload = None
            pendencia.status = "reprovado"
            db.session.commit()
            flash(f"Pendência reprovada. Motivo: {motivo}", "error")
            return redirect(url_for("pendencias.lista_pendencias"))

        doc1 = Doc1(**{k: v for k, v in form_data.items() if k in Doc1.__table__.columns})
        doc2 = Doc2(**{k: v for k, v in form_data.items() if k in Doc2.__table__.columns})
        doc3 = Doc3(**{k: v for k, v in form_data.items() if k in Doc3.__table__.columns})

        doc4 = Doc4(
            aprovado='sim' if aprovado else 'nao',
            motivo=motivo,
            **{k: v for k, v in form_data.items() if k in Doc4.__table__.columns}
        )

        db.session.add_all([doc1, doc2, doc3, doc4])
        db.session.commit()

        pessoa = Pessoa.save_pessoa(
            nome=form_data.get("nome"),
            cpf=form_data.get("cpf"),
            telefone=form_data.get("celular"),
            data_nasc=datetime.strptime(form_data.get("data_nascimento"), "%Y-%m-%d").date()
            if form_data.get("data_nascimento") else None,
            email=form_data.get("email")
        )

        voluntario = Voluntario.save_voluntario(pessoa_id=pessoa.id)

        doc = pendencia.documentacao
        doc.voluntario_id = voluntario.id
        doc.doc1_id = doc1.id
        doc.doc2_id = doc2.id
        doc.doc3_id = doc3.id
        doc.doc4_id = doc4.id
        db.session.commit()

        pendencia.payload = None
        pendencia.status = "aprovado"
        db.session.commit()

        flash("Pendência aprovada e documentação vinculada ao novo voluntário!", "success")
        return redirect(url_for("pendencias.lista_pendencias"))

    dados = {
        "nome": data.get("nome"),
        "data_nascimento": data.get("data_nascimento"),
        "local_nascimento": data.get("local_nascimento"),
        "cpf": data.get("cpf"),
        "email": data.get("email"),
        "estado_civil": data.get("estado_civil"),
        "nome_conjuge": data.get("nome_conjuge"),
        "nome_pai": data.get("nome_pai"),
        "nome_mae": data.get("nome_mae"),

        "endereco_residencial": data.get("endereco_residencial"),
        "numero": data.get("numero"),
        "bairro": data.get("bairro"),
        "cidade": data.get("cidade"),
        "cep": data.get("cep"),

        "tel_residencial": data.get("tel_residencial"),
        "celular": data.get("celular"),
        "telefone_trabalho": data.get("telefone_trabalho"),

        "religiao": data.get("religiao"),
        "escolaridade_curso": data.get("escolaridade_curso"),
        "local_trabalho": data.get("local_trabalho"),
        "ocupacao": data.get("ocupacao"),
        "ocupacao_outro_texto": data.get("ocupacao_outro_texto"),
        "tratamento_saude": data.get("tratamento_saude"),
        "tratamento_saude_para": data.get("tratamento_saude_para"),
        "transporte": data.get("transporte"),
        "como_soube_voluntariado": data.get("como_soube_voluntariado"),

        "ja_trabalhou_voluntario": data.get("ja_trabalhou_voluntario"),
        "ja_trabalhou_voluntario_onde": data.get("ja_trabalhou_voluntario_onde"),
        "faz_parte_grupo_voluntariado": data.get("faz_parte_grupo_voluntariado"),
        "qual_grupo_voluntariado": data.get("qual_grupo_voluntariado"),
        "contribuicao_voluntariado": data.get("contribuicao_voluntariado"),
        "habilidade_musical": data.get("habilidade_musical"),
        "qual_habilidade_musical": data.get("qual_habilidade_musical"),
        "auxiliar_alimentacao": data.get("auxiliar_alimentacao"),
    }

    dias_semana = ["segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo"]

    for dia in dias_semana:
        inicio = data.get(f"{dia}_inicio")
        fim = data.get(f"{dia}_fim")

        if inicio is not None:
            dados[f"{dia}_inicio"] = inicio
        if fim is not None:
            dados[f"{dia}_fim"] = fim

    return render_template("avaliacao.html", pendencia=pendencia, dados=dados)