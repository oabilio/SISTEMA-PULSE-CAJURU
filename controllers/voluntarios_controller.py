# controllers/voluntarios_controller.py
from flask import Blueprint, request, render_template, redirect, flash
from flask_login import login_required
from models.user.pessoa import Pessoa
from models.voluntarios.voluntario import Voluntario
from models.voluntarios.atividade import Atividade
from models.voluntarios.ponto import Ponto
from models.db import db

voluntarios_bp = Blueprint("voluntarios", __name__, template_folder="../views")

@voluntarios_bp.route('/voluntarios')
@login_required
def voluntarios():
    todos_voluntarios = Voluntario.query.order_by(Voluntario.pessoa_id).all()
    
    pontos_abertos = Ponto.get_pontos_abertos()
    voluntarios_ativos = [p.voluntario for p in pontos_abertos]

    return render_template(
        "voluntarios.html", 
        voluntarios=todos_voluntarios,
        voluntarios_ativos=voluntarios_ativos
    )

@voluntarios_bp.route('/cadastrar_voluntario', methods=['GET', 'POST'])
@login_required
def cadastrar_voluntario():
    if request.method == "POST":
        pessoa_id = request.form.get("pessoa_id")
        codigo_rfid = request.form.get("codigo_rfid") or None

        Voluntario.save_voluntario(pessoa_id=pessoa_id, codigo_rfid=codigo_rfid)
        #flash("Voluntário cadastrado com sucesso!")
        return redirect("/voluntarios")

    pessoas_disponiveis = Pessoa.query.filter(Pessoa.voluntario == None).all()
    return render_template("cadastro_voluntario.html", pessoas=pessoas_disponiveis)

@voluntarios_bp.route('/associar_atividade', methods=['GET', 'POST'])
@login_required
def associar_atividade():
    if request.method == "POST":
        voluntario_id = request.form.get("voluntario_id")
        atividade_id = request.form.get("atividade_id")

        voluntario = Voluntario.query.get(voluntario_id)
        atividade = Atividade.query.get(atividade_id)

        if not voluntario or not atividade:
            #flash("Voluntário ou atividade inválidos.")
            return redirect("/associar_atividade")

        if atividade not in voluntario.funcoes:
            voluntario.atividades.append(atividade)
            db.session.commit()
            #flash(f"Função '{funcao.nome}' associada ao voluntário '{voluntario.pessoa.nome}'.")
        #else:
            #flash("O voluntário já possui esta atividade.")

        return redirect("/associar_atividade")

    voluntarios = Voluntario.query.filter_by(status="ativo").all()
    atividades = Atividade.query.filter_by(ativo=True).all()
    return render_template("associar_atividade.html", voluntarios=voluntarios, atividades=atividades)

@voluntarios_bp.route('/editar_voluntario/<int:voluntario_id>', methods=['GET', 'POST'])
@login_required
def editar_voluntario(voluntario_id):
    voluntario = Voluntario.query.get_or_404(voluntario_id)
    atividades_disponiveis = Atividade.query.filter_by(ativo=True).all()

    if request.method == 'POST':
        voluntario.codigo_rfid = request.form.get('codigo_rfid') or voluntario.codigo_rfid
        voluntario.status = request.form.get('status') or voluntario.status

        atividades_selecionadas = request.form.getlist('atividades')
        voluntario.atividades = [Atividade.query.get(f) for f in atividades_selecionadas if Atividade.query.get(f)]

        db.session.commit()
        #flash("Voluntário atualizado com sucesso!")
        return redirect("/voluntarios")

    return render_template(
        "editar_voluntario.html",
        voluntario=voluntario,
        atividades_disponiveis=atividades_disponiveis
    )

@voluntarios_bp.route('/deletar_voluntario/<int:voluntario_id>', methods=['GET'])
@login_required
def deletar_voluntario(voluntario_id):
    voluntario = Voluntario.query.get(voluntario_id)
    if not voluntario:
        #flash("Voluntário não encontrado.")
        return redirect("/voluntarios")
    
    #nome_voluntario = voluntario.pessoa.nome if voluntario.pessoa else "Desconhecido"

    db.session.delete(voluntario)
    db.session.commit()

    #flash(f"Voluntário '{nome_voluntario}' deletado com sucesso!")
    return redirect("/voluntarios")