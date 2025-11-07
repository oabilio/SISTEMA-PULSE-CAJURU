from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from models.db import db
from models.voluntarios.ponto import Ponto
from models.voluntarios.voluntario import Voluntario
from datetime import datetime

ponto_bp = Blueprint("ponto", __name__, template_folder="../views")


@ponto_bp.route("/ponto")
@login_required
def ponto():
    pontos_fechados = Ponto.get_pontos_fechados(limit=100)
    pontos_abertos = Ponto.get_pontos_abertos()

    return render_template(
        "ponto.html", pontos_fechados=pontos_fechados, pontos_abertos=pontos_abertos
    )


@ponto_bp.route("/ponto/registrar_saida/<int:ponto_id>", methods=["POST"])
@login_required
def registrar_saida(ponto_id):
    ponto = Ponto.get_ponto_by_id(ponto_id)
    if ponto and ponto.saida is None:
        ponto.saida = datetime.now()
        ponto.observacao = (
            ponto.observacao or ""
        ) + "\nSaída registrada manualmente pelo sistema."
        ponto.origem = "Manual (Saída)"
        db.session.commit()
    return redirect(url_for("ponto.ponto"))


@ponto_bp.route("/ponto/manual", methods=["GET", "POST"])
@login_required
def registrar_ponto_manual():
    if request.method == "POST":
        voluntario_id = request.form.get("voluntario_id")
        entrada_str = request.form.get("entrada")
        saida_str = request.form.get("saida")
        observacao = request.form.get("observacao")

        if not voluntario_id:
            flash("Por favor, selecione um voluntário.", "error")
        elif not entrada_str:
            flash("Por favor, informe a data e hora de entrada.", "error")
        else:
            try:
                entrada_obj = datetime.fromisoformat(entrada_str)
                saida_obj = datetime.fromisoformat(saida_str) if saida_str else None

                if saida_obj and saida_obj < entrada_obj:
                    flash(
                        "A data de saída não pode ser anterior à data de entrada.",
                        "error",
                    )
                else:
                    novo_ponto = Ponto(
                        id_voluntario=int(voluntario_id),
                        entrada=entrada_obj,
                        saida=saida_obj,
                        observacao=observacao,
                        origem="Manual",
                    )
                    db.session.add(novo_ponto)
                    db.session.commit()
                    flash("Registro manual de ponto salvo com sucesso.", "success")
                    return redirect(url_for("ponto.ponto"))

            except ValueError:
                flash("Formato de data ou hora inválido.", "error")
            except Exception as e:
                db.session.rollback()
                flash(f"Erro ao salvar no banco de dados: {e}", "error")

    voluntarios = Voluntario.query.filter_by(status="ativo").all()
    return render_template("registrar_ponto_manual.html", voluntarios=voluntarios)


@ponto_bp.route("/ponto/editar/<int:ponto_id>", methods=["GET", "POST"])
@login_required
def editar_ponto(ponto_id):
    ponto = Ponto.get_ponto_by_id(ponto_id)
    if not ponto:
        flash("Registro de ponto não encontrado.", "error")
        return redirect(url_for("ponto.ponto"))

    if request.method == "POST":
        try:
            entrada_str = request.form.get("entrada")
            saida_str = request.form.get("saida")
            observacao = request.form.get("observacao")

            ponto.entrada = datetime.fromisoformat(entrada_str)
            ponto.saida = datetime.fromisoformat(saida_str) if saida_str else None
            ponto.observacao = observacao
            ponto.origem = "Manual (Editado)"

            if ponto.saida and ponto.saida < ponto.entrada:
                flash(
                    "A data de saída não pode ser anterior à data de entrada.", "error"
                )
                raise ValueError("Data de saída inválida")

            db.session.commit()
            flash("Registro de ponto atualizado com sucesso.", "success")
            return redirect(url_for("ponto.ponto"))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar: {e}", "error")
            pass

    return render_template("editar_ponto.html", ponto=ponto)


@ponto_bp.route("/ponto/deletar/<int:ponto_id>", methods=["POST"])
@login_required
def deletar_ponto(ponto_id):
    ponto = Ponto.get_ponto_by_id(ponto_id)
    if ponto:
        db.session.delete(ponto)
        db.session.commit()
        flash("Registro de ponto deletado com sucesso.", "success")
    else:
        flash("Registro de ponto não encontrado.", "error")
    return redirect(url_for("ponto.ponto"))
