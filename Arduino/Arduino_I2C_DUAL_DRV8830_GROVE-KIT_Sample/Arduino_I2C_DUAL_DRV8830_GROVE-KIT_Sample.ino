/***
 * 作成日: 2022-01-11 11:12
 * 作成者: hirotaka42
 * 概要:
 * DRV8830 I2C DUALモータドライバを使用したサンプルプログラム
 * 
 * 購入場所: 株式会社スイッチサイエンス
 * https://www.switch-science.com/catalog/2510/
 * モジュール名: I2Cモータードライバ・モジュール DRV8830 メーカー品番：DRV8830
 * 商品名     : GROVE - I2C ミニモータードライバ
 * 税込価格   : 1個 1,672 円
 */

#include <Wire.h>

#define _MOTER_R_I2C 0x65
#define _MOTER_L_I2C 0x60
// 速度(上位6bit=0x0F=0b001111=1.20V) 回転制御(下位2bit=0b01=正転5v:0b11=ブレーキ:0b10=逆転3v)
// 速度(上位6bit=0x32=0b110010=4.02V) 回転制御(下位2bit=0b01=正転5v:0b11=ブレーキ:0b10=逆転3v)
#define _SPEED 0b11001001
#define _STOP  0b11001011

void Moter_run();
void Moter_stop();

void setup() {
  // I2C 初期設定
  Wire.begin();

}


void loop() {
  // put your main code here, to run repeatedly:
  Moter_run();
  delay(5000);
  Moter_stop();
  delay(5000);

}


void Moter_run() {
/***
 * 関数名: Moter_run
 * 概要: モータを正転させる
 * 引数: None
 * return: None
 */

 char MOTER_I2C[2] = {_MOTER_R_I2C,_MOTER_L_I2C};
 
 for(int i=0;i<2;i++){   
    // 送信を開始　I2Cデバイスのアドレス
    Wire.beginTransmission(MOTER_I2C[i]);
    //　命令書き込み
    // 1-レジスタアドレス
    Wire.write(0x00);
    // 2-送信するデータ　速度(上位6bit) 回転制御(下位2bit=0b01=正転)
    Wire.write( _SPEED);
    // 送信を終了
    Wire.endTransmission();
  }
  
}


void Moter_stop() {
/***
 * 関数名: Moter_stop
 * 概要: モータを停止させる
 * 引数: None
 * return: None
 */
 
 char MOTER_I2C[2] = {_MOTER_R_I2C,_MOTER_L_I2C};
 
 for(int i=0;i<2;i++){  
    // 送信を開始　I2Cデバイスのアドレス
    Wire.beginTransmission(MOTER_I2C[i]); 
    //　命令書き込み
    // 1-レジスタアドレス
    Wire.write(0x00);
    // 2-送信するデータ　速度(上位6bit=0x0F=0b001111=1.20V) 回転制御(下位2bit=0b11=ブレーキ)
    Wire.write(_STOP);
    // 送信を終了
    Wire.endTransmission();
    
  }
  
}
