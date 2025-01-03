from bluepy import btle
import struct

#Broadcastデータ取得用デリゲート
class SwitchbotScanDelegate(btle.DefaultDelegate):
    #コンストラクタ
    def __init__(self, macaddr):
        btle.DefaultDelegate.__init__(self)
        #センサデータ保持用変数
        self.sensorValue = None
        self.macaddr = macaddr

    # スキャンハンドラー
    def handleDiscovery(self, dev, isNewDev, isNewData):
        # 対象Macアドレスのデバイスが見つかったら
        if dev.addr == self.macaddr:
            batt_flg = 0
            # アドバタイズデータを取り出し
            for (adtype, desc, value) in dev.getScanData():  
                #環境センサのとき、データ取り出しを実行
                if desc == '16b Service Data' or desc == 'Manufacturer':
                    # センサデータを取り出し
                    valueStrLength = len(value)
                    # バッテリー情報取得共通処理
                    if adtype == 22:
                        valueBinary = bytes.fromhex(value[4:])
                        batt = valueBinary[2] & 0b01111111
                        batt_flg = 1
                    # 温湿度計の場合
                    if valueStrLength == 16:
                        # 文字列からセンサデータ(4文字目以降)のみ取り出し、バイナリに変換
                        # バッテリー情報取得済ならスキップ
                        if batt_flg == 0:
                            valueBinary = bytes.fromhex(value[4:])
                            #バイナリ形式のセンサデータを数値に変換
                            batt = valueBinary[2] & 0b01111111
                        isTemperatureAboveFreezing = valueBinary[4] & 0b10000000
                        temp = ( valueBinary[3] & 0b00001111 ) / 10 + ( valueBinary[4] & 0b01111111 )
                        if not isTemperatureAboveFreezing:
                            temp = -temp
                        humid = valueBinary[5] & 0b01111111
                        #dict型に格納
                        self.sensorValue = {
                            'SensorType': 'SwitchBot',
                            'Temperature': temp,
                            'Humidity': humid,
                            'BatteryVoltage': batt
                        }
                        break
                    # CO2センサーの場合
                    elif valueStrLength == 36:
                        valueBinary = bytes.fromhex(value[16:])
                        co2 = valueBinary[7]*256 + valueBinary[8]
                        isTemperatureAboveFreezing = valueBinary[3] & 0b10000000
                        temp = ( valueBinary[2] & 0b00001111 ) / 10 + ( valueBinary[3] & 0b01111111 )
                        if not isTemperatureAboveFreezing:
                            temp = -temp
                        humid = valueBinary[4] & 0b01111111
                        # バッテリー情報取得のため処理を継続
                        continue
                    if batt_flg == 1:
                        self.sensorValue = {
                             'SensorType': 'SwitchBot',
                             'Temperature': temp,
                             'Humidity': humid,
                             'CO2': co2,
                             'BatteryVoltage': batt
                         }
