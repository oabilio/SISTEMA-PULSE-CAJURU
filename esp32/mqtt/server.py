import paho.mqtt.client as mqtt
import time

# Configuração MQTT
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativas/samuel/espparapc"
MQTT_TOPIC_RECEIVE = "exp.criativas/samuel/pcparaesp"

# Callback executado quando uma mensagem MQTT é recebida
def on_message(client, userdata, message):
    print("Frase recebida do ESP:", message.payload.decode())
    
    # Atualiza hora atual no momento da requisição
    hora_atual = time.localtime()
    hora_str = "{:02d}:{:02d}".format(hora_atual[3], hora_atual[4])  # formato HH,MM
    
    print("Enviando resposta pra esp:", hora_str)
    client.publish(MQTT_TOPIC_SEND, hora_str)  # Envia resposta

# Configuração do cliente MQTT
client = mqtt.Client("pc_samuel_20082025")
client.on_message = on_message

# Conexão ao broker MQTT e subscrição aos tópicos
client.connect(MQTT_BROKER)
client.subscribe(MQTT_TOPIC_RECEIVE)

print("Conectado ao broker, aguardando mensagens...")

# Loop principal
while True:
    client.loop(timeout=0.1)