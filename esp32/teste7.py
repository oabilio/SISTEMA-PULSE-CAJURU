from mfrc522 import MFRC522
from i2c_lcd import I2cLcd
from machine import Pin, SoftI2C, SPI
from umqtt.simple import MQTTClient
import network
import json
import time

last_msg = None

MQTT_CLIENT_ID = "esp32_samuel_20082025"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_PUBLISH = "exp.criativas/samuel/pcparaesp"
MQTT_TOPIC_SUBSCRIBE = "exp.criativas/samuel/espparapc"
MQTT_TOPIC_COMMAND = "pulse/system/command"
WIFI_SSID = "Marco AP Repet"
WIFI_PASSWORD = "M75D7457"

current_state = "MODE_SELECT"
input_buffer = ""
current_voluntario_id = None

def callback(topic_bytes, msg_bytes):
    global last_msg, current_state, current_voluntario_id
    
    topic = topic_bytes.decode()
    
    try:
        if topic == MQTT_TOPIC_SUBSCRIBE:
            last_msg = json.loads(msg_bytes.decode())
            print("[ESP] Resposta Servidor:", last_msg)
            
        elif topic == MQTT_TOPIC_COMMAND:
            print("[ESP] Comando Recebido:", msg_bytes.decode())
            data = json.loads(msg_bytes.decode())
            
            if data.get("command") == "start_registration":
                current_voluntario_id = data.get("voluntario_id")
                nome = data.get("nome_voluntario", "Voluntario")
                
                if current_voluntario_id:
                    current_state = "REGISTER_TAG_1"
                    lcd.clear()
                    lcd.putstr(f"Registrar {nome}")
                    lcd.move_to(0, 1)
                    lcd.putstr("Aproxime a Tag 1")
                    play_sound(True)
                
    except Exception as e:
        print("[ESP] Erro ao decodificar msg:", e)
        last_msg = {"status": "erro", "msg": "Erro de formato"}

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
print("Conectando à rede Wi-Fi...")
while not wifi.isconnected():
    pass
print("Conectado à rede Wi-Fi:", WIFI_SSID)

client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
client.set_callback(callback)

# --- INÍCIO DA NOVA LÓGICA DE CONEXÃO ---
def connect_and_subscribe():
    print("Conectando ao MQTT...")
    while True:
        try:
            client.connect()
            client.subscribe(MQTT_TOPIC_SUBSCRIBE)
            client.subscribe(MQTT_TOPIC_COMMAND)
            print("Conectado ao MQTT e escutando tópicos.")
            lcd.clear()
            lcd.putstr("CONECTADO")
            time.sleep(1)
            show_mode_select_screen()
            return
        except OSError as e:
            print(f"Falha ao conectar: {e}")
            lcd.clear()
            lcd.putstr("ERRO DE REDE")
            lcd.move_to(0, 1)
            lcd.putstr("Tentando em 5s..")
            time.sleep(5)
# --- FIM DA NOVA LÓGICA DE CONEXÃO ---

buzzer = Pin(2, Pin.OUT)

DEFAULT_I2C_ADDR = 0x3f
i2c = SoftI2C(scl=Pin(22, Pin.OUT, Pin.PULL_UP),
              sda=Pin(21, Pin.OUT, Pin.PULL_UP),
              freq=400000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

class Keypad:
    def __init__(self, rows_pins, cols_pins, keys):
        self.rows_pins = [Pin(pin, Pin.OUT) for pin in rows_pins]
        self.cols_pins = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in cols_pins]
        self.keys = keys
        self.last_key = None
        self.last_key_time = 0

    def scan(self):
        key = None
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_key_time) < 200:
            return None
        for r_idx, row_pin in enumerate(self.rows_pins):
            row_pin.value(0)
            for c_idx, col_pin in enumerate(self.cols_pins):
                if col_pin.value() == 0:
                    key = self.keys[r_idx][c_idx]
                    while col_pin.value() == 0:
                        time.sleep_ms(10)
                    self.last_key = key
                    self.last_key_time = current_time
                    row_pin.value(1)
                    return key
            row_pin.value(1)
        return None

KEY_MAP = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]
KEYPAD_ROWS = [25, 26, 27, 14]
KEYPAD_COLS = [12, 13, 32]
keypad = Keypad(KEYPAD_ROWS, KEYPAD_COLS, KEY_MAP)

spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)

def play_sound(success=True):
    if success:
        buzzer.value(1); time.sleep(0.1); buzzer.value(0)
    else:
        for i in range(2):
            buzzer.value(1); time.sleep(0.1); buzzer.value(0); time.sleep(0.1)

def send_and_wait(payload_dict, wait_text="ENVIANDO..."):
    global last_msg
    last_msg = None
    
    try:
        client.publish(MQTT_TOPIC_PUBLISH, json.dumps(payload_dict))
    except OSError as e:
        print(f"[ESP] Erro ao publicar: {e}")
        lcd.clear(); lcd.putstr("ERRO DE REDE"); lcd.move_to(0, 1); lcd.putstr("Falha ao enviar")
        play_sound(False); time.sleep(2)
        return None

    lcd.clear(); lcd.move_to(0, 0); lcd.putstr(wait_text)
    
    start_time = time.time()
    while time.time() - start_time < 7:
        try:
            client.check_msg()
        except OSError as e:
            print(f"[ESP] Erro no check_msg (wait): {e}")
            lcd.clear(); lcd.putstr("ERRO DE REDE"); lcd.move_to(0, 1); lcd.putstr("Conexao perdida")
            play_sound(False); time.sleep(2)
            return None 
            
        if last_msg:
            lcd.clear(); lcd.move_to(0, 0); lcd.putstr(last_msg.get('status', 'erro').upper())
            lcd.move_to(0, 1); lcd.putstr(last_msg.get('msg', 'Erro')[:16])
            play_sound(last_msg.get('status') == 'ok')
            time.sleep(3)
            return last_msg

    lcd.clear(); lcd.putstr("SEM RESPOSTA"); lcd.move_to(0, 1); lcd.putstr("Verifique o server")
    play_sound(False); time.sleep(3)
    return None

def read_rfid_tag():
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            card_id = "0x%02x%02x%02x%02x" %(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            print("[ESP] UID:", card_id)
            play_sound(True)
            return card_id
    return None

def show_mode_select_screen():
    global input_buffer, current_voluntario_id, current_state
    input_buffer = ""
    current_voluntario_id = None
    current_state = "MODE_SELECT"
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("1:PONTO 2:CPF")
    lcd.move_to(0, 1)
    lcd.putstr("                ")

connect_and_subscribe()

while True:
    try:
        client.check_msg()
    except OSError as e:
        print(f"Erro no check_msg principal: {e}")
        connect_and_subscribe()
        continue
    
    key = keypad.scan() 
    
    if current_state == "REGISTER_TAG_1":
        card_id = read_rfid_tag()
        if card_id:
            payload = {
                "command": "register_tag_1", 
                "voluntario_id": current_voluntario_id, 
                "rfid": card_id
            }
            response = send_and_wait(payload, "Lendo Tag 1...")
            
            if response and response.get("status") == "ok":
                current_state = "REGISTER_TAG_2"
                lcd.clear(); lcd.putstr("REGISTRO (2/2)"); lcd.move_to(0, 1); lcd.putstr("APROXIME DE NOVO")
            else:
                show_mode_select_screen()
        
        if key == '*':
            show_mode_select_screen()

    elif current_state == "REGISTER_TAG_2":
        card_id = read_rfid_tag()
        if card_id:
            payload = {
                "command": "register_tag_2", 
                "voluntario_id": current_voluntario_id, 
                "rfid": card_id
            }
            send_and_wait(payload, "Confirmando...")
            show_mode_select_screen()
        
        if key == '*':
            show_mode_select_screen()

    elif current_state == "MODE_SELECT":
        if key == '1':
            current_state = "RFID_SCAN"
            lcd.clear(); lcd.putstr("BATER PONTO:"); lcd.move_to(0, 1); lcd.putstr("APROXIME A TAG")
        elif key == '2':
            current_state = "CPF_ENTRY"
            input_buffer = ""
            lcd.clear(); lcd.putstr("PONTO POR CPF:"); lcd.move_to(0, 1); lcd.putstr("                ")

    elif current_state == "CPF_ENTRY":
        if key:
            if key == '#': 
                if len(input_buffer) > 0:
                    payload = {"command": "log_cpf", "cpf": input_buffer}
                    send_and_wait(payload, "Buscando CPF...")
                show_mode_select_screen()
            elif key == '*': 
                show_mode_select_screen()
            elif key.isdigit():
                input_buffer += key
                lcd.move_to(0, 1); lcd.putstr("*" * len(input_buffer)) 

    elif current_state == "RFID_SCAN":
        if key == '*':
            show_mode_select_screen()
        
        card_id = read_rfid_tag()
        if card_id:
            payload = {"command": "log_rfid", "rfid": card_id}
            send_and_wait(payload, "Buscando RFID...")
            show_mode_select_screen()

    time.sleep_ms(50)