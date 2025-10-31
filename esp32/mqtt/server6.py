import paho.mqtt.client as mqtt
import time
import json
from data6 import find_user_by_cpf, find_user_by_rfid 

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativas/samuel/espparapc"
MQTT_TOPIC_RECEIVE = "exp.criativas/samuel/pcparaesp"

def on_message(client, userdata, message):
    msg_esp = message.payload.decode()
    print("Recebido do ESP:", msg_esp)
    
    nome = None
    identificador_lido = None
    
    if msg_esp.startswith("CPF:"):
        cpf_digitado = msg_esp.split(":")[1]
        identificador_lido = cpf_digitado
        nome, cpf_encontrado = find_user_by_cpf(cpf_digitado)
    
    elif msg_esp.startswith("0x"):
        rfid_lido = msg_esp
        identificador_lido = rfid_lido
        nome, cpf_encontrado = find_user_by_rfid(rfid_lido)
        
    else:
        payload = {
            "status": "erro",
            "rfid": msg_esp,
            "msg": "Mensagem invalida"
        }
        client.publish(MQTT_TOPIC_SEND, json.dumps(payload))
        return

    if nome:
        hora_atual = time.localtime()
        hora_str = "{:02d}:{:02d}".format(hora_atual[3], hora_atual[4])

        payload = {
            "status": "ok",
            "rfid": identificador_lido,
            "nome": nome,
            "msg": f"Welcome! {hora_str}"
        }
        client.publish(MQTT_TOPIC_SEND, json.dumps(payload))
    
    else:
        payload = {
            "status": "erro",
            "rfid": identificador_lido,
            "msg": "Access Denied!"
        }
        client.publish(MQTT_TOPIC_SEND, json.dumps(payload))

client = mqtt.Client("pc_samuel_20082025")
client.on_message = on_message

client.connect(MQTT_BROKER)
client.subscribe(MQTT_TOPIC_RECEIVE)

print("Conectado ao broker, aguardando mensagens...")

while True:
    client.loop(timeout=0.1)