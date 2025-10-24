# More details can be found in TechToTinker.blogspot.com 
# George Bantique | tech.to.tinker@gmail.com

from mfrc522 import MFRC522
from i2c_lcd import I2cLcd
from machine import Pin
from machine import SoftI2C
from machine import SPI
from umqtt.simple import MQTTClient
import network
import json
import time

last_msg = None

MQTT_CLIENT_ID = "esp32_samuel_20082025"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativas/samuel/pcparaesp"
MQTT_TOPIC_RECEIVE = "exp.criativas/samuel/espparapc"

WIFI_SSID = "Marco AP Repet"
WIFI_PASSWORD = "M75D7457"

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

spi = SPI(2, baudrate=2500000, polarity=0, phase=0)

spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)

print("[ESP] Place card")

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Scan RFID")

while True:
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("RFID: ")
            
            card_id = "0x%02x%02x%02x%02x" %(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            print("[ESP] UID:", card_id)
            lcd.putstr(card_id)
            client.publish(MQTT_TOPIC_SEND, "sistema pulse")

            client.publish(MQTT_TOPIC_SEND, card_id)

            start_time = time.time()
            last_msg = None

            while time.time() - start_time < 5:
                client.check_msg()

                if last_msg:
                    lcd.clear()
                    lcd.move_to(0, 0)
                    lcd.putstr(f"{card_id}")
                    lcd.move_to(0, 1)

                    if last_msg["status"] == "ok":
                        nome = last_msg.get("nome", "")
                        msg = last_msg.get("msg", "Welcome!")
                        lcd.putstr(f"{nome} - {msg}"[:16])
                        buzzer.value(1)
                        time.sleep(0.1)
                        buzzer.value(0)
                    else:
                        lcd.putstr(last_msg["msg"][:16])
                        for i in range(2):
                            buzzer.value(1)
                            time.sleep(0.1)
                            buzzer.value(0)
                            time.sleep(0.1)
                    break