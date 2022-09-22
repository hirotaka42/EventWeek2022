#!/bin/bash

which python3

echo "venv(仮想環境) を作成 \n 以下をコピペして実行\n ↓ ↓ ↓ ↓ ↓"
echo "python3 -m venv venv"
echo "source ./venv/bin/activate"
echo "python3 -m pip install --upgrade pip"
echo "pip install -r requirements.txt"
echo "\n\n終了するには以下をコピペ実行仮想環境を終了\n ↓ ↓ ↓ ↓ ↓"
echo "deactivate"
echo "\n\n再度実行するには以下をコピペ実行し仮想環境を有効化\n ↓ ↓ ↓ ↓ ↓"
echo "source ./venv/bin/activate"


echo "sudo bluetoothctl              ... Bluetooth CTLを起動"
echo "remove D4:F0:57:D8:01:AE  ... 一旦ペアリング情報を削除"
echo "scan on                   ... デバイスをスキャン [CHG] Device XX:XX:XX:XX:XX:XX Name: Joy-Con (R) ジョイコン発見"
echo "pair D4:F0:57:D8:01:AE    ... 見つかったデバイスに対してペアリング要求"
echo "connect D4:F0:57:D8:01:AE ... connect"
echo "trust D4:F0:57:D8:01:AE   ... 次回起動時に自動接続できるよう、trustする"
echo "# プログラム実行(送信機:Publisher)"
echo "python3 PubJoycon.py"

