"""
概要    ：自動掘削機(ショベル)の制御プログラム
要求定義 :
>_ 掘削機の使用モータを構造化し、1掘削機ごとに違う動作または同じ動作をさせる
"""


import RPi.GPIO as GPIO
import Adafruit_PCA9685
from time import sleep
import threading

# Adafruit_PCA9685 を使った初期設定
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

# 使用モータの信号ピン番号
M1 = 8
R1 = 9
L1 = 10
S1 = 11

M2 = 12
R2 = 13
L2 = 14
S2 = 15

# 辞書型で簡易的に構造化
# moter_dict[i]["Moter"][n][1] の数値はモータ初期位置で使用する角度
moter_dict = [
    {"Moter":[
        [M1,10],
        [R1,150],
        [L1,160],
        [S1,90]
    ]
    },
    {"Moter":[
        [M2,10],
        [R2,150],
        [L2,160],
        [S2,90]
    ]
    }
]


def DegToPulse(deg):
    """
    引数で受けた角度をパルスに変換し、角度分サーボを回転させる
    Args  : 角度 deg 
    Return: パルス変換された角度 convert_deg_to_pulse
    メモ: 
    """
    max_pulse_pca = 610
    # 620から アーム部分のServoから変な音が出る
    min_pulse_pca = 150
    one_pulse_pca = (max_pulse_pca-min_pulse_pca)/180
    convert_deg_to_pulse = (one_pulse_pca * deg) + min_pulse_pca
    # デバッグ
    # print('deg:' + str(deg) + '(' + str(round(convert_deg_to_pulse,2)) + ')')
    return round(convert_deg_to_pulse)


def ServoRun(pin, deg):
    """
    角度分Servoを移動させる
    Args  : pin, deg
    Return: None
    """
    pwm.set_pwm(pin, 0, DegToPulse(deg))


def ServoInit():
    """
    ショベル2台のサーボ 初期キャリブレーション
    Args  : None
    Return: None
    """
    global moter_dict
    for i in range(len(moter_dict)):
        for n in range(len(moter_dict[i]["Moter"])):
            # pinと角度を引数で渡す
            ServoRun(moter_dict[i]["Moter"][n][0],moter_dict[i]["Moter"][n][1])


def ServoMotion(pin,start,end,flag):
    """
    モーション動作のプログラム
    Args   : 
    pin   -> サーボの制御ピン番号
    start -> 現在の角度
    end   -> 終了時の目的位置角度
    flag  -> 0(正転) 1(逆回転)

    Return : None

    """
    if flag == 0:
        # 正転
        for i in range(start,end):
            ServoRun(pin,i)
            sleep(0.005)
    elif flag == 1:
        # 逆回転
        for i in reversed(range(end,start)):
            ServoRun(pin,i)
            sleep(0.005)
    

def ExcavatorMotion1(SelectMoterNum:int):
    """
    ショベル(Excavator)を動かすモーション
    Args   : 
    SelectMoterNum(int)-> 動かしたいモータ集合体の番号[0,1,2,...]
    Return : None
    """
    global moter_dict

    M = moter_dict[SelectMoterNum]["Moter"][0][0]
    R = moter_dict[SelectMoterNum]["Moter"][1][0]
    L = moter_dict[SelectMoterNum]["Moter"][2][0]
    S = moter_dict[SelectMoterNum]["Moter"][3][0]
    
    cnt = 0
    while True:
        print("土台回転スタート\n  10 ->  60")
        ServoMotion(M,10,60,0)
        sleep(1)
        print("右サーボ回転スタート\n 150 -> 180")
        ServoMotion(R,150,180,0)
        sleep(1)
        print("先端サーボ回転スタート\n  90 -> 180")
        ServoMotion(S,90,180,0)
        sleep(1)
        # すくって上げる
        print("右サーボ回転スタート\n 180 -> 150")
        ServoMotion(R,180,150,1)
        sleep(1)
        print("土台回転スタート\n  60 ->  10")
        ServoMotion(M,60,10,1)
        sleep(1)
        print("先端サーボ回転スタート\n 180 ->  90")
        ServoMotion(S,180,90,1)
        sleep(1)
        cnt+=1
        print("---------------------")
        print("---------------------")
        print(f"{cnt}" + "回目終了")
        print("---------------------")
        print("---------------------")
        

def Thread_motion1():
    ExcavatorMotion1(0)

def Thread_motion2():
    ExcavatorMotion1(1)


def main():
    # スレッドを使用し ExcavatorMotionを複数台同時に実行する
    Excavator1 = threading.Thread(target=Thread_motion1)
    Excavator2 = threading.Thread(target=Thread_motion2)
    Excavator1.start()
    Excavator2.start()


if __name__ == "__main__":
    ServoInit()
    main()