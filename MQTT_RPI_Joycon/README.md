# MQTTとjoyconを用いた遠隔制御のプログラム

## 概要:
CloudMQTTを用いてjooyconの操作を
PublisherからSubscriverへ送るプログラム

- joyconPub.py からメッセージをBrokerへtopic宛にSend
- joyconSub.py でtopicを建てBrokerからtopic宛のメッセージを受信し制御

本プログラムにおいて、TLS/SSL 通信におけるCAはRPIのCAを使用しています.    
適宜パスを置き換えてください.

[How do I connect using TLS/SSL? ↗︎](https://www.cloudmqtt.com/docs/faq.html)


## 関係図:

- 役職
    - 担当機体
    - ->概要
- Publisher
    - RPI(joyconPub.py) or Websocket UI(CloudMQTT console内に存在)でも代用可能
    - ->joyconのボタンデータを(Brokerへ)送信 
- Broker
    - CloudMQTT 
    - ->別のクライアント(Publisher)からの要求(topic)に従ってデータを(Subscriverへ)送信
- Subscriver
    - RPI(joyconSub.py)
    - ->Brokerからデータを受け取り制御

## 処理の流れ

    - joyconのボタンデータがjoyconPub.pyを通じてCloud上のbroker(CloudMQTT)へ送信、
    - Cloud上のbroker(CloudMQTT)は,送信されてきたtopic宛Subscriver(joyconSub.py)にボタンデータを送信
    - Subscriver(joyconSub.py)は自分のtopic宛に送られたデータを受信し制御へ

## 使用の仕方

```bash:
# Step 1
# python venv環境(仮想化)と仮想化環境にモジュールのインストール
python3 -m venv venv && \
source ./venv/bin/activate && \
python3 -m pip install --upgrade pip && \
pip install -r requirements.txt

# Step 2
# プログラム実行(受信機:Subscriver)
python3 joyconSub.py

# Step 3
# Bluetooth接続を先に実行し接続を確認してから
#Bluetooth 接続手順
sudo bluetoothctl              ... Bluetooth CTLを起動
remove D4:F0:57:D8:01:AE  ... 一旦ペアリング情報を削除
scan on                   ... デバイスをスキャン [CHG] Device XX:XX:XX:XX:XX:XX Name: Joy-Con (R) ジョイコン発見
pair D4:F0:57:D8:01:AE    ... 見つかったデバイスに対してペアリング要求
connect D4:F0:57:D8:01:AE ... connect
trust D4:F0:57:D8:01:AE   ... 次回起動時に自動接続できるよう、trustする
# プログラム実行(送信機:Publisher)
python3 joyconPub.py


# 終了時
deactivate

# 2回目以降のvenv環境の再有効化
source ./venv/bin/activate
python3 gpioled.py
```

## 実行時

1. プログラム実行時、client.subscribe("SubscriberNAME")で設定した"SubscriberNAME"でメッセージを受信するために待機状態になります.

2. PublisherであるjoyconPub.pyで操作したjoyconボタンデータがCloudBroker(CloudMQTT)を介して,Subscriber(joyconSub.py)宛にSendされます. 

3. Subscriber宛にSendされたメッセージはbyteで送られてくるため,UTF-8でデコードしメッセージの内容に応じて条件分岐などで処理をしてあげます.


ここまでが本プログラムの一連の流れです.

