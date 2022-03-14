from wsgiref.simple_server import make_server
import json
from smbus2 import SMBus
import threading
from time import sleep

"""
アクセスがあるたびに最新のセンサデータをjsonで返却
Threadを活用し,センサーデータ取得と返却を別に
ras4b.local:3000
"""
#Jsonのデータ数
_INFO_SUM = 2
# i2cのアドレス
i2c_addr = 0x45
# SMBusモジュールの設定
bus = SMBus(1)
# i2c通信の設定     
bus.write_byte_data(i2c_addr, 0x21, 0x30)
sleep(1)


GLOBAL_SHT31 = [[0,0]]


def SHT31():
    """
    # SHT31(温湿度センサ)の測定(取得)
    Args  : None
    Return: dict型[temperature,pressure] 
    """

    bus.write_byte_data(i2c_addr, 0xE0, 0x00)
    data = bus.read_i2c_block_data(i2c_addr, 0x00, 6)

    # 温度計算
    temp_mlsb = ((data[0] << 8) | data[1])
    temp = -45 + 175 * int(str(temp_mlsb), 10) / (pow(2, 16) - 1)

    # 湿度計算
    humi_mlsb = ((data[3] << 8) | data[4])
    humi = 100 * int(str(humi_mlsb), 10) / (pow(2, 16) - 1)
    return [temp, humi]

def ThreadSHT31():
    """
    Threadを使用しセンサデータを取得後 グローバル変数のList型GLOBAL_SHT31に格納していく
    Args  : None
    Return: None
    概要   :
    格納数が50件を超えたら40件削除する
    list内容:
    [[25.45, 27.67], [25.35, 27.56], ...]
    """
    global GLOBAL_SHT31
    try:
        while True:
            print("ThreadSHT31():")
            data = SHT31()
            GLOBAL_SHT31.append([round(data[0], 2),round(data[1], 2)])
            #print(GLOBAL_SHT31)
            sleep(2)

    except KeyboardInterrupt:
        # 測定終了
        bus.write_byte_data(i2c_addr, 0x21, 0x30)
        print( "Finish!" )



    

def getData():
    """
    GLOBAL_SHT31に格納してある最新のデータを取得する
    Args   : None
    Return : list型
    概要    :
    関数ThreadSHT31で貯めたデータのうち一番新しいデータを取得し、list型で返却する
    データ内容:
    [25.42, 27.33]
    """
    global GLOBAL_SHT31
    data = GLOBAL_SHT31

    if data is None:
        result = data[1]
    else:
        result = data[-1]
    
    return result
        


def app(environ, start_response):
    """
    最新の気温と湿度データをapiとしてJsonで配信する
    データ内容:
    {
        "temperature": "25.56",
        "pressure": "27.07"
    }

    """
    status = '200 OK'
    headers = [
        ('Content-type', 'application/json; charset=utf-8'),
        ('Access-Control-Allow-Origin', '*'),
    ]
    start_response(status, headers)

    data = getData()
    sht31_dict = {'temperature': str(data[0]), 'pressure': str(data[1])}

    return [json.dumps(sht31_dict, indent=int(_INFO_SUM), ensure_ascii=False).encode("utf-8")]

def Thread_server_run():
    """
    3000番ポートでサーバを起動

    """
    with make_server('', 3000, app) as httpd:
            print("Serving on port 3000...")
            httpd.serve_forever()


def main():
    getSHT31 = threading.Thread(target=ThreadSHT31)
    ApiServer = threading.Thread(target=Thread_server_run)
    getSHT31.start()
    ApiServer.start()
    


if __name__ == "__main__":
    main()



