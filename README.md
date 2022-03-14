# HEW2022

## 概要

`IoT` x `モビリティ` x `安全性` x `Society 5.0` をテーマにした 人とインターネットの可能性を表現するプロジェクト    

制作理由：    
- 現場作業や危険な場所での作業を遠隔地から安全に操作することによって、作業者の`危険`を少しでも排除したい,コンペとして自分達に出来ることを探し挑戦しました.

取り組んだ内容:    
- 現場の俯瞰
   - カメラを使用した全体の状況把握
   - 車体や現場に取り付けたセンサデータを収集し操縦者へリアルタイムでの可視化 
- 遠隔操作
   - IoT通信プロトコル MQTTを用いたlowコストかつ低遅延な通信の実装
   - 学内コンペとして他学科にも興味を持ってもらう為に Nintendo SwitchのJoyconを使用した遠隔操作の実装
   - 学内のネット通信が混む時間帯を狙った操作遅延のテスト
- 今までにない新たな取り組み
   - Oculus Qust2 を用いたVR空間からの情報の表示
   - Unity を用いてM5StickC-Plusのセンサを応用したデータの可視化


## 使用の仕方
    各ページに記載があります。

## ディレクトリ紹介

- ディレクトリ名
    - 概要
    - README.MD LINK
- Automation/Excavator
    - 自動掘削機(ショベル)の制御プログラム
    - [Open ↗︎](./RPI/Automation/Excavator/)
- DRV8830_Joycon
    - Bluetooth制御のプログラム
    - [README.MD ↗︎](./RPI/DRV8830_Joycon/README.md)
- MQTT/MQTT_SubPub
    - MQTTを用いた遠隔制御(テスト)プログラム
    - [README.MD ↗︎](./RPI/MQTT/MQTT_SubPub/README.md)
- MQTT/MQTT_SubPub_Joycon
    - MQTTとJoyconを用いた遠隔制御(送受信)プログラム
    - [README.MD ↗︎](./RPI/MQTT/MQTT_SubPub_Joycon/README.md)
- MQTT/MQTT_Subscribe_LED
    - MQTTを用いた遠隔制御(テスト)プログラム
    - [README.MD ↗︎](./RPI/MQTT/MQTT_Subscribe_LED/README.md)
- Senser/BME280
    - 温湿度,気圧,測定プログラム
    - [Open ↗︎](./RPI/Senser/BME280/)
- Senser/SHT31
    - 温湿度,測定プログラム
    - [Open ↗︎](./RPI/Senser/SHT31/)
- Web/HTML/CameraView
    - Cmeraデータ表示のViewのみ(フロント開発で組込み予定)
    - [Open ↗︎](./Web/HTML/CameraView)





```bash:Tree
 .
├──  .gitignore
├──  Arduino
│  └──  Arduino_I2C_DUAL_DRV8830_GROVE-KIT_Sample
├──  README.md
├──  RPI
│  ├──  Automation
│  │  └──  Excavator
│  ├──  DRV8830_Joycon
│  ├──  image
│  │  └──  et.png
│  ├──  MQTT
│  │  ├──  MQTT_SubPub
│  │  ├──  MQTT_SubPub_Joycon
│  │  └──  MQTT_Subscribe_LED
│  ├──  README.md
│  ├──  Senser
│  │  ├──  BME280
│  │  └──  SHT31
│  └──  Server
└──  Web
   └──  HTML
      └──  CameraView

```