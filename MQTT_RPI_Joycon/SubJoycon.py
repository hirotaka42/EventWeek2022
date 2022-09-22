import random
import paho.mqtt.client as mqtt
from smbus2 import SMBus
import os
import sys
os.environ["SDL_VIDEODRIVER"] = "dummy"


"""
Joycon Sub
Brokerからデータを受信し,I2Cに命令を送るSubscriverプログラム

"""

"""初期設定：適宜書き換え"""
tls_ca = '/etc/ssl/certs/ca-certificates.crt'
broker = '接続先ブローカのホストネーム'
port = SSLポート番号
topic = "python/mqtt"
# generate client ID with pub prefix randomly
#client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'ユーザ名'
password = 'パスワード'
"""初期設定：適宜書き換え"""


class InitClass:
    """
    初期設定クラス
    """

    def __init__(self):
        self._MOTER_R_I2C = 0x65
        self._MOTER_L_I2C = 0x60
        self.i2c = SMBus(1) 
        #SMBusの引数に1を指定する(なぜ？)
        #i2c検出 sudo i2cdetect -y 1 の "1"でi2cデバイスが見つかったため
        """
        Usage: i2cdetect [-y] [-a] [-q|-r] I2CBUS [FIRST LAST]
            i2cdetect -F I2CBUS
            i2cdetect -l
        I2CBUS is an integer or an I2C bus name
        If provided, FIRST and LAST limit the probing range.

        pi in front in ~ via 🐍 v2.7.16 via  254MiB/365MiB | 12MiB/100MiB 
        ❯$ sudo i2cdetect -l                                     
        i2c-1   i2c             bcm2835 (i2c@7e804000)                  I2C adapter
        
        raspberryPi3A+においてI2CBusは "i2c-1"を使用していた
        """
        

    def input_method(self,Flag,Bit):
        """
        Arg: Flag-> 0:STOP, 1:UP,  2:DOWN,
                    3:RIGHT,5:UP-R,7:DOWN-R,
                    4:LEFT, 6:UP-L,8:DOWN-L,
             Bit -> 停止:0xCB 正転:0xC9 逆転:0xCA
             説明:   DRV8830には、CONTORLレジスタ,FAULTレジスタがあります.
                    1:CONTORLレジスタに動作(正転,逆転,ブレーキ・惰走)と電圧(速度)を書き込むとモータが回転します.
                    2:動作論理表:
                    IN1:IN2:OUT1:OUT2:機能
                     0 : 0 : Z  : Z  :スタンバイ/惰走
                     0 : 1 : L  : H  :逆走
                     1 : 0 : Z  : L  :正転
                     1 : 1 : H  : H  :ブレーキ

                    3:電圧表
                    [P9のTable 1. Commanded Output Voltageを参考](https://www.tij.co.jp/jp/lit/ds/symlink/drv8830.pdf)
                    今回以下の組み合わせで使用
                    [機能 2bit]  :[電圧]               :[レジスタ書き込み値 8bit] 
                    正転   =0b10 : 4.02V=0x32=0b110010 :0b11001010=0xCA (電圧bitに対し2bit左シフトし機能bitを足す)
                    逆走   =0b01 : 4.02V=0x32=0b110010 :0b11001001=0xC9 (電圧bitに対し2bit左シフトし機能bitを足す)
                    ブレーキ=0b11 : 4.02V=0x32=0b110010 :0b11001011=0xCB (電圧bitに対し2bit左シフトし機能bitを足す)

        Return: None
        概要:引数Flag の値によって回転動作を処理する
        """
        
        if Flag == "STOP" or Flag == "UP" or Flag == "DOWN":
            self.i2c.write_byte_data(self._MOTER_R_I2C, 0, Bit)
            self.i2c.write_byte_data(self._MOTER_L_I2C, 0, Bit)
        elif Flag == "RIGHT" or Flag == "UP-R" or Flag == "DOWN-R":
            self.i2c.write_byte_data(self._MOTER_R_I2C, 0, 0xCB)
            self.i2c.write_byte_data(self._MOTER_L_I2C, 0, Bit)
        elif Flag == "LEFT" or Flag == "UP-L" or Flag == "DOWN-L":
            self.i2c.write_byte_data(self._MOTER_R_I2C, 0, Bit)
            self.i2c.write_byte_data(self._MOTER_L_I2C, 0, 0xCB)

        
class SettingClass:
    """
    モーターの動作設定クラス
    """

    def __init__(self):
        # InitClassのインスタンスを作成する
        self.initClass = InitClass()
    
    def FW_method(self):
        """
        概要:前に進む 
        """
        self.initClass.input_method("UP",0xC9)
        print("Run FW_method")
        

    def Rear_method(self):
        """
        概要:後ろに進む 
        """
        self.initClass.input_method("DOWN",0xCA)
        print("Run Rear_method")


    def R_method(self):
        """
        概要:Rに進む 
        """
        self.initClass.input_method("RIGHT",0xC9)
        print("Run R_method")
        

    def L_method(self):
        """
        概要:Lに進む 
        """
        self.initClass.input_method("LEFT",0xC9)
        print("Run L_method")

    def Rear_R_method(self):
        """
        """
        self.initClass.input_method("DOWN-R",0xCA)
        print("Run Rear_R_method")

    def Rear_L_method(self):
        """
        """
        self.initClass.input_method("DOWN-L",0xCA)
        print("Run Rear_L_method")

    def STOP_method(self):
        """
        elif event.type == pygame.JOYHATMOTION and event.value == (0, 0):
        """
        self.initClass.input_method("STOP",0xCB)
        print("Stop")


def control_i2c(bytesmsg):
    """

    """
    msg = bytesmsg.decode('utf-8')
    #SettingClassのインスタンスを作成
    setClass = SettingClass()

    print(msg)
    if msg == "FW":
        setClass.FW_method()
    elif msg == "ST":
        setClass.STOP_method()
    elif msg == "RE":
        setClass.Rear_method()
    elif msg == "L":
        setClass.L_method()
    elif msg == "R":
        setClass.R_method()
    elif msg == "RR":
        setClass.Rear_R_method()
    elif msg == "RL":
        setClass.Rear_L_method()
    else :
        setClass.STOP_method()
    

def connect_mqtt() -> mqtt:
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


def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        control_i2c(msg.payload)


    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()


