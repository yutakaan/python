from bluepy import btle
from subfunc.switchbot import SwitchbotScanDelegate
from subfunc import env
from subfunc import linefunc
from subfunc import logfunc
from subfunc import token
import datetime
import os
import sys

# set LINE
LINE_URL = linefunc.URL
ACCESS_TOKEN = token.ACCESS_TOKEN
HEADERS = linefunc.HEADERS
SEND_FLAG = sys.argv[1]
LINE_MESSAGE = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' 取得'
TIME_HH = datetime.datetime.now().strftime("%H")

# set log
LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'thermoCO2meter.log')
logger = logfunc.get_logger(__name__, LOG_TXT)

# set Mac Address
MACADDRESS = str.lower(env.THERMO_CO2_MAC)

######SwitchBotの値取得######
def main():    
    logger.info('Start ThermoCO2Meter')
    contents = getThermometer(MACADDRESS)
    if SEND_FLAG == '1':
        linefunc.pushLine(LINE_URL, ACCESS_TOKEN, HEADERS, contents)
    logger.info('Stop ThermoCO2Meter')

def getThermometer(macaddress):
    #switchbot.pyのセンサ値取得デリゲートを、スキャン時実行に設定
    scanner = btle.Scanner().withDelegate(SwitchbotScanDelegate(macaddress))
    #スキャンしてセンサ値取得（タイムアウト5秒）
    scanner.scan(5.0)

    temp = 'Tempreture = ' + str( scanner.delegate.sensorValue['Temperature'])
    logger.debug(temp)
    humi = 'Humidity = ' + str( scanner.delegate.sensorValue['Humidity'])
    logger.debug(humi)
    co2 = 'CO2 = ' + str( scanner.delegate.sensorValue['CO2'])
    logger.debug(co2)
    bat = 'Battery = ' + str( scanner.delegate.sensorValue['BatteryVoltage'] )
    logger.debug(bat)

    contents = '\n' + temp + '\n' + humi + '\n' + co2 + '\n' + bat

    return contents

if __name__=='__main__':
    main()
