from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_login import login_required
from models.user.pessoa import Pessoa
from models.voluntarios.voluntario import Voluntario
from models.voluntarios.atividade import Atividade
from models.db import db
from sqlalchemy.exc import IntegrityError
import paho.mqtt.publish as publish
import json

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_COMMAND = "pulse/system/command"

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
        
        vol = Voluntario.save_voluntario(pessoa_id=pessoa_id, codigo_rfid=None)
        
        flash("Voluntário cadastrado! Agora, associe um RFID.", "success")
        return redirect(url_for('voluntarios.editar_voluntario', voluntario_id=vol.id))

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
            flash("Voluntário ou atividade inválidos.", "error")
            return redirect("/associar_atividade")

        if atividade not in voluntario.atividades:
            voluntario.atividades.append(atividade)
            db.session.commit()
            flash(f"Atividade '{atividade.nome}' associada.", "success")
        else:
            flash("O voluntário já possui esta atividade.", "info")
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
        voluntario.status = request.form.get('status') or voluntario.status
        atividades_selecionadas = request.form.getlist('atividades')
        voluntario.atividades = [Atividade.query.get(f) for f in atividades_selecionadas if Atividade.query.get(f)]

        db.session.commit()
        flash("Voluntário atualizado com sucesso!", "success")
        return redirect(url_for('voluntarios.editar_voluntario', voluntario_id=voluntario.id))

    return render_template(
        "editar_voluntario.html",
        voluntario=voluntario,
        atividades_disponiveis=atividades_disponiveis
    )

@voluntarios_bp.route('/voluntario/<int:voluntario_id>/start_rfid_register', methods=['POST'])
@login_required
def start_rfid_register(voluntario_id):
    voluntario = Voluntario.query.get_or_404(voluntario_id)
    
    if voluntario.codigo_rfid:
         flash(f"Este voluntário já possui um RFID. Limpe o RFID antes de registrar um novo.", "error")
         return redirect(url_for('voluntarios.editar_voluntario', voluntario_id=voluntario.id))
         
    try:
        payload = {
            "command": "start_registration",
            "voluntario_id": voluntario.id,
            "nome_voluntario": voluntario.pessoa.nome.split()[0]
        }
        
        publish.single(MQTT_TOPIC_COMMAND, json.dumps(payload), hostname=MQTT_BROKER)
        
        flash(f"Comando enviado ao leitor! Por favor, aproxime a tag 2x...", "success")
    except Exception as e:
        flash(f"Erro ao enviar comando para o leitor: {e}. Verifique o MQTT.", "error")

    return redirect(url_for('voluntarios.editar_voluntario', voluntario_id=voluntario.id))

@voluntarios_bp.route('/voluntario/<int:voluntario_id>/limpar_rfid', methods=['POST'])
@login_required
def limpar_rfid(voluntario_id):
    voluntario = Voluntario.query.get_or_404(voluntario_id)
    voluntario.codigo_rfid = None
    db.session.commit()
    flash("Código RFID removido. Agora você pode registrar um novo.", "success")
    return redirect(url_for('voluntarios.editar_voluntario', voluntario_id=voluntario.id))

@voluntarios_bp.route('/deletar_voluntario/<int:voluntario_id>', methods=['POST'])
@login_required
def deletar_voluntario(voluntario_id):
    voluntario = Voluntario.query.get(voluntario_id)
    if not voluntario:
        flash("Voluntário não encontrado.", "error")
        return redirect("/voluntarios")
    
    nome_voluntario = voluntario.pessoa.nome if voluntario.pessoa else "Desconhecido"

    try:
        if voluntario.pontos:
            flash(f"Não é possível deletar {nome_voluntario}. Ele(a) possui registros de ponto associados.", "error")
            return redirect("/voluntarios")
        
        if voluntario.movimentacoes:
            flash(f"Não é possível deletar {nome_voluntario}. Ele(a) possui movimentações associadas.", "error")
            return redirect("/voluntarios")

        voluntario.atividades = []
        db.session.commit()
        
        db.session.delete(voluntario)
        db.session.commit()

        flash(f"Voluntário '{nome_voluntario}' deletado com sucesso!", "success")
    
    except IntegrityError:
        db.session.rollback()
        flash(f"Erro de integridade: Não foi possível deletar {nome_voluntario}. Verifique se ele(a) não está associado(a) a um Usuário.", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro inesperado ao deletar: {e}", "error")
            
    return redirect("/voluntarios")