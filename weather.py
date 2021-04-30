import requests
import os
import sys
from subfunc import logfunc
from subfunc import jsonfunc
from subfunc import linefunc
from subfunc import token

# set logger
LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'weather.log')
logger = logfunc.get_logger(__name__, LOG_TXT)

# set weather func
URL = jsonfunc.WEATHER_URL
DATE_MODE = jsonfunc.DATE_MODE
AREA_MODE = jsonfunc.AREA_MODE

# set line func
LINE_URL = linefunc.URL
ACCESS_TOKEN = token.ACCESS_TOKEN
HEADERS = linefunc.HEADERS

logger.info('start weather.py')

# get weather data
def getWeatherData():
    logger.debug('start weather api')
    tenki_data = jsonfunc.getWeather(URL)
    logger.debug('end weather api')

    # get weather info
    m_title = tenki_data[0]['publishingOffice']
    m_date = tenki_data[0]['timeSeries'][0]['timeDefines'][DATE_MODE]
    m_date = m_date[0:10]
    m_area = tenki_data[0]['timeSeries'][0]['areas'][AREA_MODE]['area']['name']
    m_weather = tenki_data[0]['timeSeries'][0]['areas'][AREA_MODE]['weathers'][DATE_MODE]

    # get precip
    num = len(tenki_data[0]['timeSeries'][1]['timeDefines'])
    l_precip = [0] *4
    j = 0

    for i in range(num):
        tmp_date = tenki_data[0]['timeSeries'][1]['timeDefines'][i]
        if m_date == tmp_date[0:10]:
            l_precip[j] = tenki_data[0]['timeSeries'][1]['areas'][AREA_MODE]['pops'][j]
            j = j + 1

    # get temprature
    m_max = tenki_data[0]['timeSeries'][2]['areas'][AREA_MODE]['temps'][1]
    m_min = tenki_data[0]['timeSeries'][2]['areas'][AREA_MODE]['temps'][0]

    # make message
    MESSAGE = '\n' + m_title + '\n' \
              + m_area + 'の' + m_date + 'の天気'  + '\n' \
              + '天気：' + m_weather + '\n' \
              + '降水確率' + '\n' \
              + '   0時〜6時：' + l_precip[0] + '%' + '\n' \
              + '  6時〜12時：' + l_precip[1] + '%' + '\n' \
              + ' 12時〜18時：' + l_precip[2] + '%' + '\n' \
              + ' 18時〜24時：' + l_precip[3] + '%' + '\n' \
              + '最高気温：' + m_max + '度' + '\n' \
              + '最低気温：' + m_min + '度'

    logger.debug(m_title + ',' + m_area + ',' + m_date + ',' + m_weather + ',' + l_precip[0] + ',' + l_precip[1] + ',' + l_precip[2] + ',' + l_precip[3] + ',' + m_max + ',' + m_min)

    return MESSAGE

def main():
    logger.info('start weather.py')
    LINE_MESSAGE = getWeatherData()
    linefunc.pushLine(LINE_URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE)
    logger.info('end weather.py')

if __name__=='__main__':
    main()
