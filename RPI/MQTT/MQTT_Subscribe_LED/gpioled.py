import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

"""
概要:
CloudMQTTを使用した遠隔操作のテストプログラム
Publisher からのデータに応じてLED(GPIO22Pin)をON/OFFします.
本プログラムにおいて、RPIはSubscriverの役割を果たします

関係図:
Publisher  : RPI or Websocket UI(CloudMQTT console内に存在)
->データを(Brokerへ)送信 
Subscriver : RPI
->Brokerからデータを受け取る
Broker     : CloudMQTT 
->別のクライアント(Subscriver等)からの要求に従ってデータを(Publisherへ)送信

"""
 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("isjp/gpio22")
 
def on_message(client, userdata, msg):
     print(msg.topic+" "+str(msg.payload))
     print(msg.payload.decode('utf-8'))
     if msg.payload.decode('utf-8') == "on":
         GPIO.output(22,1)
         print("GPIO.output(22,1)")
     else:
         GPIO.output(22,0)
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.tls_set("/etc/ssl/certs/ca-certificates.crt")
client.username_pw_set("USERNAME", "PASSWD")
client.connect("SERVER", SSLPORT)
 
client.loop_forever()