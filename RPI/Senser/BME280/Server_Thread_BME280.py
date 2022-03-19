"""
BME280を使用したセンサー値を配信するServerプログラム

要求定義:
アクセスがあるたびに最新のセンサデータをjsonで返却
Threadを活用し,センサーデータ取得と返却を別に
ras4b.local:3000
"""
from wsgiref.simple_server import make_server
import json
from smbus2 import SMBus
import threading
from time import sleep

#Jsonのデータ数
_INFO_SUM = 3
# リングバッファ参照用 変数
GLOBAL_buffer = 0
GLOBAL_bottom = 0

class RingBuffer:
    """
    リングバッファ クラス
    Args : size(int) バッファサイズ

    """
    def __init__(self, size):
        global GLOBAL_buffer 
        global GLOBAL_bottom
        GLOBAL_buffer = [None for i in range(0, size)]
        self.top = 0
        GLOBAL_bottom = 0
        self.size = size

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

    def view_all_data(self):
        global GLOBAL_buffer 
        print(GLOBAL_buffer)

class BME280:

    def __init__(self):
        self.digT = []
        self.digP = []
        self.digH = []
        self.t_fine = 0.0
        bus_number  = 1
        # i2cのアドレス
        self.i2c_addr = 0x76
        # SMBusモジュールの設定
        self.bus = SMBus(bus_number)
        # デバッグ
        #print("class init OK")
        self.setup()
        # デバッグ
        #print("class init setup OK")

    def writeReg(self, reg_addr, data):
        """
        I2Cに命令を書き込む関数
        Args:
        reg_addr-> コマンド,
        data    -> 書き込みたいデータ,

        """
        self.bus.write_byte_data(self.i2c_addr,reg_addr,data)

    
    def setup(self):
        osrs_t = 1			#Temperature oversampling x 1
        osrs_p = 1			#Pressure oversampling x 1
        osrs_h = 1			#Humidity oversampling x 1
        mode   = 3			#Normal mode
        t_sb   = 5			#Tstandby 1000ms
        filter = 0			#Filter off
        spi3w_en = 0			#3-wire SPI Disable

        ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | mode
        config_reg    = (t_sb << 5) | (filter << 2) | spi3w_en
        ctrl_hum_reg  = osrs_h

        self.writeReg(0xF2,ctrl_hum_reg)
        self.writeReg(0xF4,ctrl_meas_reg)
        self.writeReg(0xF5,config_reg)


    def get_calib_param(self):
        calib = []
        
        for i in range (0x88,0x88+24):
            calib.append(self.bus.read_byte_data(self.i2c_addr,i))
        calib.append(self.bus.read_byte_data(self.i2c_addr,0xA1))
        for i in range (0xE1,0xE1+7):
            calib.append(self.bus.read_byte_data(self.i2c_addr,i))

        self.digT.append((calib[1] << 8) | calib[0])
        self.digT.append((calib[3] << 8) | calib[2])
        self.digT.append((calib[5] << 8) | calib[4])
        self.digP.append((calib[7] << 8) | calib[6])
        self.digP.append((calib[9] << 8) | calib[8])
        self.digP.append((calib[11]<< 8) | calib[10])
        self.digP.append((calib[13]<< 8) | calib[12])
        self.digP.append((calib[15]<< 8) | calib[14])
        self.digP.append((calib[17]<< 8) | calib[16])
        self.digP.append((calib[19]<< 8) | calib[18])
        self.digP.append((calib[21]<< 8) | calib[20])
        self.digP.append((calib[23]<< 8) | calib[22])
        self.digH.append( calib[24] )
        self.digH.append((calib[26]<< 8) | calib[25])
        self.digH.append( calib[27] )
        self.digH.append((calib[28]<< 4) | (0x0F & calib[29]))
        self.digH.append((calib[30]<< 4) | ((calib[29] >> 4) & 0x0F))
        self.digH.append( calib[31] )
        
        for i in range(1,2):
            if self.digT[i] & 0x8000:
                self.digT[i] = (-self.digT[i] ^ 0xFFFF) + 1

        for i in range(1,8):
            if self.digP[i] & 0x8000:
                self.digP[i] = (-self.digP[i] ^ 0xFFFF) + 1

        for i in range(0,6):
            if self.digH[i] & 0x8000:
                self.digH[i] = (-self.digH[i] ^ 0xFFFF) + 1  

    

    def compensate_P(self,adc_P)->str:
        """
        気圧を求める関数
        Args  : adc_P(センサー(気圧部分)のRAWデータ)
        Return: 997.33 (:.2f)->str
        """
        pressure = 0.0
        
        v1 = (self.t_fine / 2.0) - 64000.0
        v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * self.digP[5]
        v2 = v2 + ((v1 * self.digP[4]) * 2.0)
        v2 = (v2 / 4.0) + (self.digP[3] * 65536.0)
        v1 = (((self.digP[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8)  + ((self.digP[1] * v1) / 2.0)) / 262144
        v1 = ((32768 + v1) * self.digP[0]) / 32768
        
        if v1 == 0:
            return 0
        pressure = ((1048576 - adc_P) - (v2 / 4096)) * 3125
        if pressure < 0x80000000:
            pressure = (pressure * 2.0) / v1
        else:
            pressure = (pressure / v1) * 2
        v1 = (self.digP[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096
        v2 = ((pressure / 4.0) * self.digP[7]) / 8192.0
        pressure = pressure + ((v1 + v2 + self.digP[6]) / 16.0)  
        # f-stringを使用し 桁数.2fで切り取り表示
        print(f"pressure : {pressure/100:.2f} hPa")
        value = f"{pressure/100:.2f}"
        return value

    def compensate_T(self,adc_T)->str:
        """
        気温を求める関数
        Args  : adc_T(センサー(気温部分)のRAWデータ)
        Return: 21.50 (:.2f)->str
        """
        v1 = (adc_T / 16384.0 - self.digT[0] / 1024.0) * self.digT[1]
        v2 = (adc_T / 131072.0 - self.digT[0] / 8192.0) * (adc_T / 131072.0 - self.digT[0] / 8192.0) * self.digT[2]
        self.t_fine = v1 + v2
        temperature = self.t_fine / 5120.0
        print(f"temp : {temperature:.2f} 度")
        value = f"{temperature:.2f}"
        return value

    def compensate_H(self,adc_H)->str:
        """
        湿度を求める関数
        Args  : adc_H(センサー(湿度部分)のRAWデータ)
        Return: 42.98 (:.2f)->str
        """
        var_h = self.t_fine - 76800.0
        if var_h != 0:
            var_h = (adc_H - (self.digH[3] * 64.0 + self.digH[4]/16384.0 * var_h)) * (self.digH[1] / 65536.0 * (1.0 + self.digH[5] / 67108864.0 * var_h * (1.0 + self.digH[2] / 67108864.0 * var_h)))
        else:
            return 0
        var_h = var_h * (1.0 - self.digH[0] * var_h / 524288.0)
        if var_h > 100.0:
            var_h = 100.0
        elif var_h < 0.0:
            var_h = 0.0
        print(f"hum : {var_h:.2f} ％")
        value = f"{var_h:.2f}"
        return value

    def readData(self)->dict:
        """
        センサーのデータブロックからデータの読み込み,辞書型に整形し返却
        Args : self
        Return: BME280_dict
        BME280_dict = {
            'BME280': {
                'temperature': str(tmp[0]), 
                'pressure': str(tmp[1]),
                'hum': str(tmp[2])
            }
        }
        """

        # デバッグ
        # print("def readData OK")
        data = []
        tmp = []
        for i in range (0xF7, 0xF7+8):
            data.append(self.bus.read_byte_data(self.i2c_addr,i))
        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        hum_raw  = (data[6] << 8)  |  data[7]


        tmp.append(self.compensate_T(temp_raw))
        tmp.append(self.compensate_P(pres_raw))
        tmp.append(self.compensate_H(hum_raw))
        
        BME280_dict = {
            'BME280': {
                'temperature': str(tmp[0]), 
                'pressure': str(tmp[1]),
                'hum': str(tmp[2])
            }
        }

        return BME280_dict

def Thread_Senser():
    """
    センサーの値を取得しリングバッファに格納
    Args : None
    Return: None
    """
    Senser = BME280()
    rbuf = RingBuffer(5)
    Senser.get_calib_param()

    while True:
        rbuf.add(Senser.readData())
        # デバッグ
        rbuf.view_all_data()
        # センサ情報取得時に負荷を軽減させるために取得間隔を開ける
        sleep(2)

def getData()->dict:
    """
    リングバッファに格納してある最新のデータを取得する
    Args   : None
    Return : 辞書型
    概要    :
    関数ThreadSHT31で貯めたデータのうち一番新しいデータを取得し、辞書型で返却する
    データ内容:
    {'BME280': {'temperature': '20.95 ', 'pressure': '998.70 ', 'hum': '40.69 '}}
    """
    global GLOBAL_buffer
    global GLOBAL_bottom
    # クラス RingBufferにおいて新規値を addした後, bottom値を次に切り替えてしまうため、最新の値はbottom値のひとつ前に格納されている
    result = GLOBAL_buffer[GLOBAL_bottom-1]
    # デバッグ
    print("-----------")
    print("-----------")
    print(f"Debug: >>> Func:getData()-> {result}")
    print("-         -")
    print("-----------")
    return result

def app(environ, start_response):
    """
    """
    status = '200 OK'
    headers = [
        ('Content-type', 'application/json; charset=utf-8'),
        ('Access-Control-Allow-Origin', '*'),
    ]
    start_response(status, headers)
    # 最新データを
    senser_dict = getData()
    return [json.dumps(senser_dict, indent=int(_INFO_SUM), ensure_ascii=False).encode("utf-8")]

def Thread_server_run():
    """
    3000番ポートでサーバを起動
    
    """
    with make_server('', 3000, app) as httpd:
            print("Serving on port 3000...")
            httpd.serve_forever()

def main():
    getSenser = threading.Thread(target=Thread_Senser)
    ApiServer = threading.Thread(target=Thread_server_run)
    getSenser.start()
    ApiServer.start()


if __name__ == '__main__':
    main()
