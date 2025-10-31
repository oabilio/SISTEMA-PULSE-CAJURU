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
MQTT_TOPIC_SEND = "exp.criativas/samuel/pcparaesp"
MQTT_TOPIC_RECEIVE = "exp.criativas/samuel/espparapc"
WIFI_SSID = "Visitantes"
WIFI_PASSWORD = ""	

def callback(topic, msg):
    global last_msg
    last_msg = json.loads(msg.decode())
    
    status = last_msg.get("status")
    rfid = last_msg.get("rfid", "N/A")
    nome = last_msg.get("nome", "")
    mensagem = last_msg.get("msg", "")

    if status == "ok":
        print(f"[ESP] {nome} ({rfid}) - {mensagem}")
    else:
        print(f"[ESP] ({rfid}) - {mensagem}")

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
print("Conectando à rede Wi-Fi...")
while not wifi.isconnected():
    pass
print("Conectado à rede Wi-Fi:", WIFI_SSID)

client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
client.set_callback(callback)
client.connect()
client.subscribe(MQTT_TOPIC_RECEIVE)

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

def wait_for_server_response(display_id):
    global last_msg
    last_msg = None
    start_time = time.time()
    
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("ENVIANDO...")
    lcd.move_to(0, 1)
    lcd.putstr(display_id[:16])

    while time.time() - start_time < 5:
        client.check_msg()
        if last_msg:
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr(f"{last_msg.get('rfid', 'N/A')[:16]}")
            lcd.move_to(0, 1)

            if last_msg["status"] == "ok":
                nome = last_msg.get("nome", "")
                msg = last_msg.get("msg", "Welcome!")
                lcd.putstr(f"{nome} - {msg}"[:16])
                buzzer.value(1); time.sleep(0.1); buzzer.value(0)
            else:
                lcd.putstr(last_msg["msg"][:16])
                for i in range(2):
                    buzzer.value(1); time.sleep(0.1); buzzer.value(0); time.sleep(0.1)
            
            time.sleep(3)
            return

current_state = "MODE_SELECT"
input_buffer = ""

def show_mode_select_screen():
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("1: BATER PONTO")
    lcd.move_to(0, 1)
    lcd.putstr("2: DIGITAR CPF")

show_mode_select_screen()

while True:
    client.check_msg()
    
    key = keypad.scan()
    
    if current_state == "MODE_SELECT":
        if key == '1':
            current_state = "RFID_SCAN"
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("APROXIME A TAG")
            lcd.move_to(0, 1)
            lcd.putstr("*: VOLTAR")
        elif key == '2':
            current_state = "CPF_ENTRY"
            input_buffer = ""
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("DIGITE O CPF:")
            lcd.move_to(0, 1)
            lcd.putstr("#: OK | *: LIMPAR")
            time.sleep(1.5)
            lcd.move_to(0, 1)
            lcd.putstr("                ")

    elif current_state == "CPF_ENTRY":
        if key:
            if key == '#':
                if len(input_buffer) > 0:
                    print(f"[ESP] Enviando CPF: {input_buffer}")
                    client.publish(MQTT_TOPIC_SEND, f"CPF:{input_buffer}")
                    
                    wait_for_server_response(f"CPF: {input_buffer}")
                    
                    current_state = "MODE_SELECT"
                    show_mode_select_screen()
                else:
                    lcd.move_to(0, 1)
                    lcd.putstr("Digite algo!")
                    time.sleep(1)
                    lcd.move_to(0, 1)
                    lcd.putstr("                ")
                    
            elif key == '*':
                input_buffer = ""
                lcd.move_to(0, 1)
                lcd.putstr("LIMPO!            ")
                time.sleep(1)
                lcd.move_to(0, 1)
                lcd.putstr("                ")
            
            elif key.isdigit():
                input_buffer += key
                lcd.move_to(0, 1)
                lcd.putstr("*" * len(input_buffer)) 

    elif current_state == "RFID_SCAN":
        if key == '*':
            current_state = "MODE_SELECT"
            show_mode_select_screen()
        
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                card_id = "0x%02x%02x%02x%02x" %(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                print("[ESP] UID:", card_id)
                
                client.publish(MQTT_TOPIC_SEND, card_id)
                
                wait_for_server_response(card_id)
                
                current_state = "MODE_SELECT"
                show_mode_select_screen()

    time.sleep_ms(50)