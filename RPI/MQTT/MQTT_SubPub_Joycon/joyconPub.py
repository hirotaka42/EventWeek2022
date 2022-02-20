import random
import time
import paho.mqtt.client as mqtt
import pygame
"""
Joycon Publisher
概要:
Joyconのボタンデータを 
MQTTのBroker宛にsendするPublisherプログラム

"""

"""初期設定：適宜書き換え"""
tls_ca = '/etc/ssl/certs/ca-certificates.crt'
broker = '###Server###'
port = ###PORT###
topic = "python/mqtt"
# generate client ID with pub prefix randomly
#client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = '###USERNAME###'
password = '###PASSWD###'
"""初期設定：適宜書き換え"""

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.tls_set(tls_ca)
    client.username_pw_set(username, password)
    client.connect(broker, port)
    return client


def publish(client):
    
    while True:
        #time.sleep(1)
        flag_count = 0
        msg_button = ''
        #Joy-con初期化
        pygame.init()
        joys = pygame.joystick.Joystick(0)
        joys.init()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN and event.button == 1:
                msg_button = f"messages: X:1"
                #flag_count = 1
                print(event)
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 2:
                msg_button = f"messages: B:2"
                print(event)
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                msg_button = f"messages: A:0"
                print(event)
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 3:
                msg_button = f"messages: Y:3"
                print(event)
            elif event.type == pygame.JOYHATMOTION and event.value == (0, 0):
                msg_button = f"ST"
                flag_count = 1
                #setClass.STOP_method()
                print(event)
            elif event.type == pygame.JOYHATMOTION and event.value == (1, 0):
                msg_button = f"FW"
                flag_count = 1
                #setClass.FW_method()
                print(event)
            elif event.type == pygame.JOYHATMOTION and event.value == (-1, 0):
                msg_button = f"RE"
                flag_count = 1
                #setClass.Rear_method()
                print(event)
            elif event.type == pygame.JOYHATMOTION and event.value == (0, 1):
                msg_button = f"L"
                flag_count = 1
                #setClass.L_method()
            elif event.type == pygame.JOYHATMOTION and event.value == (0, -1):
                msg_button = f"R"
                flag_count = 1
                #setClass.R_method()
            elif event.type == pygame.JOYHATMOTION and event.value == (1, 1):
                msg_button = f"L"
                flag_count = 1
                #setClass.L_method()
                print(event)
            elif event.type == pygame.JOYHATMOTION and event.value == (1, -1):
                msg_button = f"R"
                flag_count = 1
                #setClass.R_method()
                print(event)
            elif event.type == pygame.JOYHATMOTION and event.value == (-1, 1):
                msg_button = f"RL"
                flag_count = 1
                #setClass.Rear_L_method()
                print(event)
            elif event.type == pygame.JOYHATMOTION and event.value == (-1, -1):
                msg_button = f"RR"
                flag_count = 1
                #setClass.Rear_R_method()
                print(event)
            else :
                pass

        
        if flag_count == 1: 
            result = client.publish(topic, msg_button)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg_button}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")

            flag_count = 0
            

        time.sleep(0.3)


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()