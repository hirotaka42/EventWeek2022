# HEW2022

## 概要

IoT x モビリティー をテーマにしたプロジェクト


## 詳細

- 車の遠隔操縦
- マスタースレーブ操作におけるスケーリング操縦
- メタバース(VR空間)と現実両方に存在する物体の同期操作




## 使用の仕方

    None

## ディレクトリ紹介

### Arduino(主にセンサー値などの取得サンプルプログラム群)

- ディレクトリ名
    - 概要
    - README.MD LINK
- Arduino/Arduino_I2C_DUAL_DRV8830_GROVE-KIT_Sample
    - DRV8830制御のテストプログラム
    - README.MD None

```bash:
├── Arduino
│   └── Arduino_I2C_DUAL_DRV8830_GROVE-KIT_Sample
│       └── Arduino_I2C_DUAL_DRV8830_GROVE-KIT_Sample.ino
```

### RPI(RaspberryPi関係)

- ディレクトリ名
    - 概要
    - README.MD LINK
- DRV8830_Joycon
    - Bluetooth制御のプログラム
    - [README.MD ↗︎](./RPI/DRV8830_Joycon/README.md)
- MQTT/MQTT_Subscribe_LED
    - MQTTを用いた遠隔制御(テスト)プログラム
    - [README.MD ↗︎](./RPI/MQTT/MQTT_Subscribe_LED/README.md)

```bash:
├── RPI
│   ├── DRV8830_Joycon
│   │   ├── DRV8830_Joycon.py
│   │   ├── README.md
│   │   ├── readme.sh
│   │   └── requirements.txt
│   └── MQTT
│       └── MQTT_Subscribe_LED
│           ├── README.md
│           ├── gpioled.py
│           ├── img
│           │   ├── gif01.gif
│           │   ├── img01.png
│           │   └── img02.png
│           ├── readme.sh
│           └── requirements.txt
```


### Web (アプリケーションやHTMLなどの単品を格納)

- ディレクトリ名
    - 概要
    - README.MD LINK
- HTML/CameraView
    - 俯瞰システムにおけるカメラ映像のWebView
    - [README.MD ↗︎](./Web/HTML/CameraView/README.md)



```bash:
└── Web
    └── HTML
        └── CameraView
            ├── README.md
            ├── css
            │   └── style.css
            ├── img
            │   ├── NoImage.png
            │   ├── cam_sub1_wh.png
            │   ├── cam_sub2.png
            │   ├── cam_sub2_wh.png
            │   ├── cam_sub3_wh.png
            │   ├── camera1.png
            │   └── camera1_wh.png
            ├── index.html
            └── index.png
```

### 全体のTree

```bash:
├── Arduino
│   └── Arduino_I2C_DUAL_DRV8830_GROVE-KIT_Sample
│       └── Arduino_I2C_DUAL_DRV8830_GROVE-KIT_Sample.ino
├── DataSheet
├── Fusion360
├── KiCAD
├── M5StickC-Plus
├── README.md
├── RPI
│   ├── DRV8830_Joycon
│   │   ├── DRV8830_Joycon.py
│   │   ├── README.md
│   │   ├── readme.sh
│   │   └── requirements.txt
│   └── MQTT
│       └── MQTT_Subscribe_LED
│           ├── README.md
│           ├── gpioled.py
│           ├── img
│           │   ├── gif01.gif
│           │   ├── img01.png
│           │   └── img02.png
│           ├── readme.sh
│           └── requirements.txt
└── Web
    └── HTML
        └── CameraView
            ├── README.md
            ├── css
            │   └── style.css
            ├── img
            │   ├── NoImage.png
            │   ├── cam_sub1_wh.png
            │   ├── cam_sub2.png
            │   ├── cam_sub2_wh.png
            │   ├── cam_sub3_wh.png
            │   ├── camera1.png
            │   └── camera1_wh.png
            ├── index.html
            └── index.png

16 directories, 24 files
```