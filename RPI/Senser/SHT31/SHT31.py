from smbus2 import SMBus
from time import sleep

# i2cのアドレス
i2c_addr = 0x45
# SMBusモジュールの設定
bus = SMBus(1)

# SHT31(温湿度センサ)の測定
def SHT31():
    bus.write_byte_data(i2c_addr, 0xE0, 0x00)
    data = bus.read_i2c_block_data(i2c_addr, 0x00, 6)

    # 温度計算
    temp_mlsb = ((data[0] << 8) | data[1])
    temp = -45 + 175 * int(str(temp_mlsb), 10) / (pow(2, 16) - 1)

    # 湿度計算
    humi_mlsb = ((data[3] << 8) | data[4])
    humi = 100 * int(str(humi_mlsb), 10) / (pow(2, 16) - 1)
    return [temp, humi]

# i2c通信の設定     
bus.write_byte_data(i2c_addr, 0x21, 0x30)
sleep(1)
try:
    while True:
        data = SHT31()
        print( str('{:.4g}'.format(data[0])) + "C" )
        print( str('{:.4g}'.format(data[1])) + "%" )
        print("------")
        sleep(1)    
except KeyboardInterrupt:
    # 測定終了
    bus.write_byte_data(i2c_addr, 0x21, 0x30)
    print( "Finish!" )