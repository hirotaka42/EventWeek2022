#!/bin/bash

which python3

echo "venv(仮想環境) を作成 \n 以下をコピペして実行してください\n ↓ ↓ ↓ ↓ ↓"
echo "python3 -m venv venv"
echo "source ./venv/bin/activate"
echo "python3 -m pip install --upgrade pip"
echo "pip install -r requirements.txt"
echo "\n\n終了するには以下をコピペ実行仮想環境を終了してください\n ↓ ↓ ↓ ↓ ↓"
echo "deactivate"
echo "\n\n再度実行するには以下をコピペ実行し仮想環境を有効化してください\n ↓ ↓ ↓ ↓ ↓"
echo "source ./venv/bin/activate"


echo "Adafruit ライブラリをインストール"
echo "git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git"
echo "git clone https://github.com/adafruit/Adafruit_Python_GPIO.git"
echo "git clone https://github.com/adafruit/Adafruit_Python_PureIO.git"


echo "cd Adafruit_Python_PCA9685"
echo "sudo python3 setup.py install"
echo "cd ../Adafruit_Python_GPIO"
echo "sudo python3 setup.py install"
echo "cd ../Adafruit_Python_PureIO"
echo "sudo python3 setup.py install"


echo "----------------------------------"
echo "sudo i2cdetect -y 1"
echo " "
echo "PCA9685は、パルス150～650が角度0～180に対応しているので以下の式を使用してパルスを出す。"
echo "pulse = ( 650 - 150 ) / 180 * 角度 + 150" 