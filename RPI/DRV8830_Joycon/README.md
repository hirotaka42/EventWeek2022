# Nintendo SWITCH用 Joy-Conを用いたモータドライバ(DRV8830)の制御

## 概要:
RPIとJoy-Conを使用したBluetooth操作のプログラム
Joy-Con からのボタンデータに応じてDRV8830(I2C)を制御します.


## 関係図:

- 役職
    - 担当機体
    - ->概要
- コントローラ
    - Joy-Con
    - ->Bluetooth接続によりボタンデータをリアルタイムに送信します
- コントローラ接続先
    - RPI
    - ->Python3プログラムからI2Cで接続している2機のモータドライバをJoy-Conからのボタンデータで制御する
- デバイス
    - DRV8830 (モータドライバ)
    - -> 左右のモータを制御するためにI2Cドライバを2機搭載(R=0x65,L=0x60)



## 処理の流れ

Joy-Conのボタンデータに応じてモータ制御を変更

```python:
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN and event.button == 1:
                print("X:1")
                print(event)
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 2:
                print("B:2")
                print(event)
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                print("A:0")
                print(event)
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 3:
                print("Y:3")
                print(event)
            elif event.type == pygame.JOYHATMOTION and event.value == (0, 0):
                setClass.STOP_method()
            elif event.type == pygame.JOYHATMOTION and event.value == (1, 0):
                setClass.FW_method()
            elif event.type == pygame.JOYHATMOTION and event.value == (-1, 0):
                setClass.Rear_method()
            elif event.type == pygame.JOYHATMOTION and event.value == (0, 1):
                print("<-")
                setClass.L_method()
            elif event.type == pygame.JOYHATMOTION and event.value == (0, -1):
                print("->")
                setClass.R_method()
            elif event.type == pygame.JOYHATMOTION and event.value == (1, 1):
                setClass.L_method()
            elif event.type == pygame.JOYHATMOTION and event.value == (1, -1):
                setClass.R_method()
            elif event.type == pygame.JOYHATMOTION and event.value == (-1, 1):
                setClass.Rear_L_method()
            elif event.type == pygame.JOYHATMOTION and event.value == (-1, -1):
                setClass.Rear_R_method()
            
        time.sleep(0.1)
```

'button'| ButtonKey |-|'button'| ButtonKey |
-|-|-|-|-|
0|A|-|9|+|
1|X|-|11|Joycon押し込み|
2|B|-|12|Home|
3|Y|-|None|None|
4|SL|-|14|R|
5|SR|-|15|ZR|

'value'| JoyHatMotion | - | 'value' | JoyHatMotion |
-|-|-|-|-|
(0,0) |中央 ・|-|(1,-1)|右上 ↗︎
(1,0)|中央上 ↑|-|(-1,-1)|右下 ↘︎
(-1,0)|中央下 ↓|-|(1,1)|左上 ↖︎
(0,1)|中央左 ←|-|(-1,1)|左下 ↙︎
(0,-1)|中央右 →|-|





## 使用の仕方

1. Joy-ConとRPIのBluetooth接続

### Bluetooth 接続手順(CLI)

```bash:
bluetoothctl              ... Bluetooth CTLを起動
remove D4:F0:57:D8:01:AE  ... 一旦ペアリング情報を削除
scan on                   ... デバイスをスキャン [CHG] Device D4:F0:57:D8:01:AE Name: Joy-Con (R) ジョイコン発見
pair D4:F0:57:D8:01:AE    ... 見つかったデバイスに対してペアリング要求
connect D4:F0:57:D8:01:AE ... connect
trust D4:F0:57:D8:01:AE   ... 次回起動時に自動接続できるよう、trustする
```

2回目以降接続ができないことが多いので起動毎にコネクションを確立する必要がある

2. python venv環境(仮想化)の作成

```bash:
# python venv環境(仮想化)と仮想化環境にモジュールのインストール
python3 -m venv venv && \
source ./venv/bin/activate && \
python3 -m pip install --upgrade pip && \
pip install -r requirements.txt

# プログラム実行
python3 DRV8830_Joycon.py

# 終了時
deactivate

# 2回目以降のvenv環境の再有効化
source ./venv/bin/activate
python3 DRV8830_Joycon.py
```

## 実行時

Bluetooth接続とI2Cのアドレス設定に問題なければプログラム実行とともにJoy-Conを用いてモータドライバの制御ができるようになっています。
ですがJoy-Conが任天堂純正ではない場合やJoy-Conの通信方式の違いにより正しく動作しない場合もあります.
その場合、プログラム内のJoy-Conボタンの値を各自のコントローラに合わせて書き換えてください.

ここまでが本プログラムの一連の流れです.