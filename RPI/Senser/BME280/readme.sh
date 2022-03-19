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
echo "----------------------------------"
echo "sudo i2cdetect -y 1"
