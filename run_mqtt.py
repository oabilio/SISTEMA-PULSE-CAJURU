# run_mqtt.py
import paho.mqtt.client as mqtt
import time
import json
import logging
from datetime import datetime

from controllers.app_controller import create_app
from models.db import db
from models.user.pessoa import Pessoa
from models.voluntarios.voluntario import Voluntario
from models.voluntarios.ponto import Ponto

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SUBSCRIBE = "exp.criativas/samuel/pcparaesp"
MQTT_TOPIC_PUBLISH = "exp.criativas/samuel/espparapc"
MQTT_CLIENT_ID = "flask_server_samuel_20082025"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Armazena a primeira tag lida, associada ao ID do voluntário
# Estrutura: { 5: "0xTagLida1" } (onde 5 é o voluntario_id)
PENDING_REGISTRATIONS = {}

def send_response(client, status, msg, rfid=None):
    payload = {
        "status": status,
        "msg": msg,
        "rfid": rfid
    }
    log.info(f"Enviando para ESP: {payload}")
    client.publish(MQTT_TOPIC_PUBLISH, json.dumps(payload))

def handle_log_rfid(client, rfid):
    rfid_tag = rfid.strip() if rfid else None
    if not rfid_tag:
        send_response(client, "erro", "Tag invalida", rfid)
        return
        
    voluntario = Voluntario.query.filter_by(codigo_rfid=rfid_tag).first()
    
    if voluntario and voluntario.status == 'ativo':
        pessoa = Pessoa.query.get(voluntario.pessoa_id)
        acao = Ponto.registrar_batida_rfid(voluntario.id, rfid_tag, "RFID")
        msg_acao = "Entrada" if acao == "entrada" else "Saida"
        send_response(client, "ok", f"{msg_acao}! {pessoa.nome.split()[0]}", rfid_tag)
    elif voluntario:
        send_response(client, "erro", "Vol. Inativo", rfid_tag)
    else:
        send_response(client, "erro", "Tag nao cadast.", rfid_tag)

def handle_log_cpf(client, cpf):
    pessoa = Pessoa.query.filter_by(cpf=cpf).first()
    
    if pessoa and pessoa.voluntario and pessoa.voluntario.status == 'ativo':
        acao = Ponto.registrar_batida_rfid(pessoa.voluntario.id, None, "CPF")
        msg_acao = "Entrada" if acao == "entrada" else "Saida"
        send_response(client, "ok", f"{msg_acao}! {pessoa.nome.split()[0]}", cpf)
    elif pessoa:
        send_response(client, "erro", "Vol. Inativo", cpf)
    else:
        send_response(client, "erro", "CPF nao cadast.", cpf)

# --- Lógica de Registro Atualizada ---

def handle_register_tag_1(client, voluntario_id, rfid):
    """ Recebe a primeira leitura de tag para um voluntário. """
    voluntario = Voluntario.query.get(voluntario_id)
    if not voluntario:
        send_response(client, "erro", "Volunt. Invalido", str(voluntario_id))
        return

    tag_existente = Voluntario.query.filter_by(codigo_rfid=rfid).first()
    if tag_existente:
        send_response(client, "erro", "Tag ja em uso!", rfid)
        return

    PENDING_REGISTRATIONS[voluntario_id] = rfid
    log.info(f"Voluntário {voluntario_id} leu a primeira tag: {rfid}")
    send_response(client, "ok", "Tag 1 OK", rfid)

def handle_register_tag_2(client, voluntario_id, rfid):
    """ Recebe a segunda leitura de tag e finaliza o registro. """
    voluntario = Voluntario.query.get(voluntario_id)
    first_tag = PENDING_REGISTRATIONS.get(voluntario_id)
    
    if not voluntario:
        send_response(client, "erro", "Volunt. Invalido", str(voluntario_id))
    elif not first_tag:
        send_response(client, "erro", "Erro. Leia tag 1", str(voluntario_id))
    elif first_tag != rfid:
        send_response(client, "erro", "Tags Diferentes", rfid)
    else:
        try:
            voluntario.codigo_rfid = rfid
            db.session.commit()
            log.info(f"SUCESSO: RFID {rfid} associado ao Voluntário {voluntario.id}")
            send_response(client, "ok", "Registrado!", rfid)
        except Exception as e:
            db.session.rollback()
            log.error(f"Erro de DB ao registrar: {e}")
            send_response(client, "erro", "Erro no servidor", rfid)
            
    PENDING_REGISTRATIONS.pop(voluntario_id, None)

def on_message(client, userdata, message):
    """Callback principal. Usa um NOVO app_context para CADA mensagem."""
    
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
                send_response(client, "erro", "Comando invalido")
                    
        except Exception as e:
            log.error(f"Erro no on_message: {e}")
            send_response(client, "erro", "Erro no formato")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("Conectado ao MQTT Broker!")
        client.subscribe(MQTT_TOPIC_SUBSCRIBE)
    else:
        log.error(f"Falha ao conectar, código {rc}")

def main():
    log.info("Iniciando o servidor MQTT integrado ao Flask...")
    
    app = create_app()
    
    client_userdata = {'app': app}
    client = mqtt.Client(MQTT_CLIENT_ID, userdata=client_userdata)
    
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER)
    except Exception as e:
        log.error(f"Não foi possível conectar ao Broker: {e}")
        return

    log.info("Servidor MQTT rodando. Aguardando mensagens do ESP32...")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        log.info("Desconectando...")
        client.disconnect()
        log.info("Servidor MQTT parado.")

if __name__ == "__main__":
    main()