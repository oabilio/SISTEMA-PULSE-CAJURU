import json
import logging
import time
from datetime import datetime
from threading import Thread

import paho.mqtt.client as mqtt
from controllers.app_controller import create_app
from flask_socketio import SocketIO
from models.db import db
from models.user.pessoa import Pessoa
from models.voluntarios.ponto import Ponto
from models.voluntarios.voluntario import Voluntario
from utils.create_db import create_db

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SUBSCRIBE = "exp.criativas/samuel/pcparaesp"
MQTT_TOPIC_PUBLISH = "exp.criativas/samuel/espparapc"
MQTT_TOPIC_COMMAND = "pulse/system/command"
MQTT_CLIENT_ID = "flask_server_samuel_20082025"

app = create_app()
socketio = SocketIO(app, async_mode='gevent')

PENDING_REGISTRATIONS = {}

def send_response_to_esp(client, status, msg, rfid=None):
    payload = { "status": status, "msg": msg, "rfid": rfid }
    log.info(f"Enviando para ESP: {payload}")
    client.publish(MQTT_TOPIC_PUBLISH, json.dumps(payload))

def handle_log_rfid(client, rfid):
    rfid_tag = rfid.strip() if rfid else None
    if not rfid_tag:
        send_response_to_esp(client, "erro", "Tag invalida", rfid)
        return

    voluntario = Voluntario.query.filter_by(codigo_rfid=rfid_tag).first()
    
    if voluntario and voluntario.status == 'ativo':
        pessoa = Pessoa.query.get(voluntario.pessoa_id)
        acao = Ponto.registrar_batida_rfid(voluntario.id, rfid_tag, "RFID")
        msg_acao = "Entrada" if acao == "entrada" else "Saida"
        
        send_response_to_esp(client, "ok", f"{msg_acao}! {pessoa.nome.split()[0]}", rfid_tag)
        socketio.emit('update_ponto', {'msg': f'Ponto registrado para {pessoa.nome}'})
        
    elif voluntario:
        send_response_to_esp(client, "erro", "Vol. Inativo", rfid_tag)
    else:
        send_response_to_esp(client, "erro", "Tag nao cadast.", rfid_tag)

def handle_log_cpf(client, cpf):
    formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    pessoa = Pessoa.query.filter_by(cpf=formatted_cpf).first()
    
    if pessoa and pessoa.voluntario and pessoa.voluntario.status == 'ativo':
        acao = Ponto.registrar_batida_rfid(pessoa.voluntario.id, None, "CPF")
        msg_acao = "Entrada" if acao == "entrada" else "Saida"
        
        send_response_to_esp(client, "ok", f"{msg_acao}! {pessoa.nome.split()[0]}", cpf)
        socketio.emit('update_ponto', {'msg': f'Ponto registrado para {pessoa.nome}'})

    elif pessoa:
        send_response_to_esp(client, "erro", "Vol. Inativo", cpf)
    else:
        send_response_to_esp(client, "erro", "CPF nao cadast.", cpf)

def handle_register_tag_1(client, voluntario_id, rfid):
    voluntario = db.session.get(Voluntario, voluntario_id)
    if not voluntario:
        send_response_to_esp(client, "erro", "Volunt. Invalido", str(voluntario_id))
        return

    tag_existente = Voluntario.query.filter_by(codigo_rfid=rfid).first()
    if tag_existente:
        send_response_to_esp(client, "erro", "Tag ja em uso!", rfid)
        return

    PENDING_REGISTRATIONS[voluntario_id] = rfid
    log.info(f"Voluntário {voluntario_id} leu a primeira tag: {rfid}")
    send_response_to_esp(client, "ok", "Tag 1 OK", rfid)
    socketio.emit('show_flash_message', {'msg': f'Tag 1 lida ({rfid}). Aproxime novamente.', 'category': 'info'})

def handle_register_tag_2(client, voluntario_id, rfid):
    voluntario = db.session.get(Voluntario, voluntario_id)
    first_tag = PENDING_REGISTRATIONS.get(voluntario_id)
    
    if not voluntario:
        send_response_to_esp(client, "erro", "Volunt. Invalido", str(voluntario_id))
    elif not first_tag:
        send_response_to_esp(client, "erro", "Erro. Leia tag 1", str(voluntario_id))
    elif first_tag != rfid:
        send_response_to_esp(client, "erro", "Tags Diferentes", rfid)
        socketio.emit('show_flash_message', {'msg': 'As tags lidas são diferentes. Tente novamente.', 'category': 'error'})
    else:
        try:
            voluntario.codigo_rfid = rfid
            db.session.commit()
            log.info(f"SUCESSO: RFID {rfid} associado ao Voluntário {voluntario.id}")
            send_response_to_esp(client, "ok", "Registrado!", rfid)
            socketio.emit('update_voluntario', {'msg': f'RFID {rfid} registrado para {voluntario.pessoa.nome}!'})
        except Exception as e:
            db.session.rollback()
            log.error(f"Erro de DB ao registrar: {e}")
            send_response_to_esp(client, "erro", "Erro no servidor", rfid)
            socketio.emit('show_flash_message', {'msg': 'Erro ao salvar no banco.', 'category': 'error'})
            
    PENDING_REGISTRATIONS.pop(voluntario_id, None)

def on_message(client, userdata, message):
    app = userdata['app']
    with app.app_context():
        try:
            msg_str = message.payload.decode()
            log.info(f"Recebido do ESP: {msg_str}")
            data = json.loads(msg_str)
            command = data.get("command")
            
            if command == "log_rfid":
                handle_log_rfid(client, data.get("rfid"))
            elif command == "log_cpf":
                handle_log_cpf(client, data.get("cpf"))
            elif command == "register_tag_1":
                handle_register_tag_1(client, data.get("voluntario_id"), data.get("rfid"))
            elif command == "register_tag_2":
                handle_register_tag_2(client, data.get("voluntario_id"), data.get("rfid"))
            else:
                send_response_to_esp(client, "erro", "Comando invalido")
                    
        except Exception as e:
            log.error(f"Erro no on_message: {e}")
            send_response_to_esp(client, "erro", "Erro no formato")
        finally:
            db.session.remove()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("Conectado ao MQTT Broker!")
        client.subscribe(MQTT_TOPIC_SUBSCRIBE)
    else:
        log.error(f"Falha ao conectar, código {rc}")

def start_mqtt_client():
    log.info("Iniciando cliente MQTT em um thread separado...")
    
    app_for_thread = create_app()
    client_userdata = {'app': app_for_thread}
    
    mqtt_client = mqtt.Client(MQTT_CLIENT_ID, userdata=client_userdata)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    try:
        mqtt_client.connect(MQTT_BROKER)
        mqtt_client.loop_forever()
    except Exception as e:
        log.error(f"Não foi possível iniciar o cliente MQTT: {e}")

if __name__ == "__main__":
    
    create_db(app) 
    
    log.info("Iniciando o servidor Flask-SocketIO...")
    
    mqtt_thread = Thread(target=start_mqtt_client)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    
    socketio.run(app, host='0.0.0.0', port=8080, debug=True, allow_unsafe_werkzeug=True, use_reloader=False)