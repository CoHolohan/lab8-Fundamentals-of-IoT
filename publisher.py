# Lab 6 – MQTT Temperature Publisher Niamh Flynn (C22388461), Eoin Keogh (C22456452), Cormac Holohan (C22363913)

import network
import time
import umqtt.simple as umqtt
from machine import ADC

SSID = "Cormac’s iPhone"
PASSWORD = "PS4Cormac"
HOSTNAME = "172.20.10.14"
PORT = 8080
TOPIC = b"temp/pico"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to Wi-Fi ...")
while not wlan.isconnected():
    time.sleep(1)
print("Connected:", wlan.ifconfig())

mqtt = umqtt.MQTTClient(
    client_id=b'publish',
    server=HOSTNAME,
    port=PORT,
    keepalive=7000
)
mqtt.connect()
print("Connected to MQTT broker at", HOSTNAME)

sensor_temp = ADC(4)
conversion_factor = 3.3 / 65535

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temp_c = 27 - (reading - 0.706) / 0.001721   
    msg = f"{temp_c:.2f}"
    print(f"Publishing temperature: {msg} °C")
    mqtt.publish(TOPIC, msg.encode())
    time.sleep(0.5)
