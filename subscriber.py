# Lab 6 – MQTT Temperature Subscriber / Fan Controller

import network
import time
import ubinascii
import machine
from machine import Pin
from umqtt.simple import MQTTClient

SSID = "Cormac’s iPhone"
PASSWORD = "PS4Cormac"
HOSTNAME = "172.20.10.14"
PORT = 8080
TOPIC = b"temp/pico"
CLIENT_ID=b'subscribe'

fan = Pin("LED", Pin.OUT)       # change to LED pin if testing

def callback(topic, msg):
    temp = float(msg.decode())
    print(f"Received: {temp:.2f} °C")
    if temp > 25:
        fan.value(1)
        print("Fan ON")
    else:
        fan.value(0)
        print("Fan OFF")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)
print("Connected to Wi-Fi:", wlan.ifconfig())

mqtt = MQTTClient(client_id=CLIENT_ID, server=HOSTNAME, port=PORT, keepalive=7000)
mqtt.set_callback(callback)
mqtt.connect()
mqtt.subscribe(TOPIC)
print("Subscribed to", TOPIC)

while True:
    mqtt.wait_msg()  


