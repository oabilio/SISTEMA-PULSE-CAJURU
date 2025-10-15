# More details can be found in TechToTinker.blogspot.com 
# George Bantique | tech.to.tinker@gmail.com

from mfrc522 import MFRC522
from i2c_lcd import I2cLcd
from machine import Pin
from machine import SoftI2C
from machine import SPI
from umqtt.simple import MQTTClient
import network
import time

MQTT_CLIENT_ID = "esp32_samuel_20082025"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativas/samuel/pcparaesp"
MQTT_TOPIC_RECEIVE = "exp.criativas/samuel/espparapc"

WIFI_SSID = "Visitantes"
WIFI_PASSWORD = ""

def callback(topic, msg):
    global last_msg
    last_msg = msg.decode()
    print("[ESP] Mensagem recebida:", last_msg)

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
# Using Hardware SPI pins:
#     sck=18   # yellow
#     mosi=23  # orange
#     miso=19  # blue
#     rst=4    # white
#     cs=5     # green, DS
# *************************
# To use SoftSPI,
# from machine import SOftSPI
# spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)

rfid_name = ["Samuel",
             "Abilio"]
rfid_uid = ["0x66d7247e",
            "0xe6877603"]

def get_username(uid):
    index = 0
    try:
        index = rfid_uid.index(uid)
        return rfid_name[index]
    except:
        index = -1
        print("RFID is not recognized")
        return 0

print("Place card")

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
            print("UID:", card_id)
            lcd.putstr(card_id)
            client.publish(MQTT_TOPIC_SEND, "sistema pulse")

            username = get_username(card_id)
            lcd.move_to(0, 1)
            if username != 0:
                buzzer.value(1)
                time.sleep(0.1) 
                buzzer.value(0) 
                time.sleep(0.1)
                lcd.putstr("Welcome {}".format(username))
                client.publish(MQTT_TOPIC_SEND, username)
                start_time = time.time()
                while time.time() - start_time < 5:
                    client.check_msg()
            else:
                lcd.putstr(" Access Denied! ")
                for i in range (2):
                    buzzer.value(1)
                    time.sleep(0.1) 
                    buzzer.value(0) 
                    time.sleep(0.1)
