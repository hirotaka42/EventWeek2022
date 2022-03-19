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


RINGSIZE = 10
GLOBAL_buffer = [None for i in range(0, RINGSIZE)]
GLOBAL_bottom = 0

class RingBuffer:
    """
    リングバッファ クラス
    Args : size(int) バッファサイズ

    """
    def __init__(self):
        global GLOBAL_buffer 
        global GLOBAL_bottom
        global RINGSIZE
        self.top = 0
        GLOBAL_bottom = 0
        self.size = RINGSIZE

    def __len__(self):
        global GLOBAL_bottom
        return GLOBAL_bottom - self.top

    def add(self, value):
        global GLOBAL_buffer 
        global GLOBAL_bottom
        # 最新のボトム番地に 値を代入
        GLOBAL_buffer[GLOBAL_bottom] = value
        # ボトム を次に進め、バッファの総配列数 で ボトムの位置を割った値を ボトムに代入
        # つまり バッファの配列数は常に一定になるので
        # 初めにバッファを5サイズにすると N=(0+1)%5 という式になり
        #  N=1,2,3,4,0,1,2..... のようなリングバッファとして使用できる、循環するボトムが完成する
        GLOBAL_bottom = (GLOBAL_bottom + 1) % len(GLOBAL_buffer)

    def get(self, index=None):
        global GLOBAL_buffer 
        if index is not None:
            return GLOBAL_buffer[index]

        value = GLOBAL_buffer[self.top]
        self.top =(self.top + 1) % len(GLOBAL_buffer)
        return value

    def get_new_data(self, index=None):
        global GLOBAL_buffer 
        if index is not None:
            return GLOBAL_buffer[index]

        value = GLOBAL_buffer[self.top]
        return value
        

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
    センサデータを取得後 グローバル変数のGLOBAL_buffer(実態はリングバッファ)に格納していく
    Args  : None
    Return: None
    概要   :
    辞書内容:
    [{'SHT31': [23.05, 54.15]}, {'SHT31': [23.06, 54.02]}, ...]
    """
    global GLOBAL_bottom
    global GLOBAL_buffer
    rbuf = RingBuffer()
    
    try:
        while True:
            print("ThreadSHT31():")
            print(GLOBAL_buffer)
            print(GLOBAL_bottom)
            data = SHT31()
            value = {
                "SHT31": [
                    round(data[0], 2),
                    round(data[1], 2)
                    ]
            }

            rbuf.add(value)
            #print(GLOBAL_SHT31)
            sleep(2)

    except KeyboardInterrupt:
        # 測定終了
        bus.write_byte_data(i2c_addr, 0x21, 0x30)
        print( "Finish!" )

   

def getData()->dict:
    """
    GLOBAL_SHT31に格納してある最新のデータを取得する
    Args   : None
    Return : 辞書型
    概要    :
    関数ThreadSHT31で貯めたデータのうち一番新しいデータを取得し、辞書型で返却する
    データ内容:
    {'SHT31': [23.06, 54.02]}
    """
    global GLOBAL_buffer
    global GLOBAL_bottom
    # クラス RingBufferにおいて新規値を addした後, bottom値を次に切り替えてしまうため、最新の値はbottom値のひとつ前に格納されている
    result = GLOBAL_buffer[GLOBAL_bottom-1]
    print("-----------")
    print("-----------")
    print("Debug:" + "Func:getData()->" + '{}'.format(result))
    print("-         -")
    print("-----------")
    return result
        

def app(environ, start_response):
    """
    最新の気温と湿度データをapiとしてJsonで配信する
    データ内容:
    {
        "SHT31": {
            "temperature": "23.06",
            "pressure": "54.02"
        }
    }
    """
    status = '200 OK'
    headers = [
        ('Content-type', 'application/json; charset=utf-8'),
        ('Access-Control-Allow-Origin', '*'),
    ]
    start_response(status, headers)
    
    data = getData()
    sht31_dict = {
        'SHT31': {
            'temperature': str(data["SHT31"][0]), 
            'pressure': str(data["SHT31"][1])
        }
    }

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



