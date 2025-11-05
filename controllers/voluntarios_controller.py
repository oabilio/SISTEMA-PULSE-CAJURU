# controllers/voluntarios_controller.py
from flask import Blueprint, request, render_template, redirect, flash
from flask_login import login_required
from models.user.pessoa import Pessoa
from models.voluntarios.voluntario import Voluntario
from models.voluntarios.funcao import Funcao
from models.db import db

voluntarios_bp = Blueprint("voluntarios", __name__, template_folder="../views")

@voluntarios_bp.route('/voluntarios')
@login_required
def voluntarios():
    voluntarios_ativos = Voluntario.query.all()
    return render_template("voluntarios.html", voluntarios=voluntarios_ativos)

@voluntarios_bp.route('/cadastrar_voluntario', methods=['GET', 'POST'])
@login_required
def cadastrar_voluntario():
    if request.method == "POST":
        pessoa_id = request.form.get("pessoa_id")
        codigo_rfid = request.form.get("codigo_rfid") or None

        Voluntario.save_voluntario(pessoa_id=pessoa_id, codigo_rfid=codigo_rfid)
        flash("Voluntário cadastrado com sucesso!")
        return redirect("/voluntarios")

    pessoas_disponiveis = Pessoa.query.filter(Pessoa.voluntario == None).all()
    return render_template("cadastro_voluntario.html", pessoas=pessoas_disponiveis)

@voluntarios_bp.route('/associar_funcao', methods=['GET', 'POST'])
@login_required
def associar_funcao():
    if request.method == "POST":
        voluntario_id = request.form.get("voluntario_id")
        funcao_id = request.form.get("funcao_id")

        voluntario = Voluntario.query.get(voluntario_id)
        funcao = Funcao.query.get(funcao_id)

        if not voluntario or not funcao:
            flash("Voluntário ou função inválidos.")
            return redirect("/associar_funcao")

        if funcao not in voluntario.funcoes:
            voluntario.funcoes.append(funcao)
            db.session.commit()
            flash(f"Função '{funcao.nome}' associada ao voluntário '{voluntario.pessoa.nome}'.")
        else:
            flash("O voluntário já possui esta função.")

        return redirect("/associar_funcao")

    voluntarios = Voluntario.query.filter_by(status="ativo").all()
    funcoes = Funcao.query.filter_by(ativo=True).all()
    return render_template("associar_funcao.html", voluntarios=voluntarios, funcoes=funcoes)

@voluntarios_bp.route('/editar_voluntario/<int:voluntario_id>', methods=['GET', 'POST'])
@login_required
def editar_voluntario(voluntario_id):
    voluntario = Voluntario.query.get_or_404(voluntario_id)
    funcoes_disponiveis = Funcao.query.filter_by(ativo=True).all()

    if request.method == 'POST':
        voluntario.codigo_rfid = request.form.get('codigo_rfid') or voluntario.codigo_rfid
        voluntario.status = request.form.get('status') or voluntario.status

        funcoes_selecionadas = request.form.getlist('funcoes')
        voluntario.funcoes = [Funcao.query.get(f) for f in funcoes_selecionadas if Funcao.query.get(f)]

        db.session.commit()
        flash("Voluntário atualizado com sucesso!")
        return redirect("/voluntarios")

    return render_template(
        "editar_voluntario.html",
        voluntario=voluntario,
        funcoes_disponiveis=funcoes_disponiveis
    )

@voluntarios_bp.route('/deletar_voluntario/<int:voluntario_id>', methods=['GET'])
@login_required
def deletar_voluntario(voluntario_id):
    voluntario = Voluntario.query.get(voluntario_id)
    if not voluntario:
        flash("Voluntário não encontrado.")
        return redirect("/voluntarios")
    
    nome_voluntario = voluntario.pessoa.nome if voluntario.pessoa else "Desconhecido"

    db.session.delete(voluntario)
    db.session.commit()

    flash(f"Voluntário '{nome_voluntario}' deletado com sucesso!")
    return redirect("/voluntarios")