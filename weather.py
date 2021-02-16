import requests
import os
import sys
from subfunc import logfunc
from subfunc import jsonfunc
from subfunc import linefunc

LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'weather.log')

URL = jsonfunc.WEATHER_URL
SITE_ID = jsonfunc.SITE_ID

LINE_URL = linefunc.URL
ACCESS_TOKEN = linefunc.ACCESS_TOKEN
HEADERS = linefunc.HEADERS

args = sys.argv
MODE = int(args[1])

logger = logfunc.get_logger(__name__, LOG_TXT)

logger.info('天気取得処理開始')
logger.debug('API実行')
tenki_data = jsonfunc.getWeather(URL, SITE_ID)
logger.debug('API終了')

m_title = tenki_data['title']
m_date = tenki_data['forecasts'][MODE]['date']
m_telop = tenki_data['forecasts'][MODE]['telop']
m_max = tenki_data['forecasts'][MODE]['temperature'].get('max')
m_min = tenki_data['forecasts'][MODE]['temperature'].get('min')
if m_max is None:
    m_max = 'None'
else:
    m_max = tenki_data['forecasts'][MODE]['temperature']['max']['celsius']

if m_min is None:
    m_min = 'None'
else:
    m_min = tenki_data['forecasts'][MODE]['temperature']['min']['celsius']

LINE_MESSAGE = '\n' + m_title + '\n' \
          + '日付：' + m_date + '\n' \
          + '天気：' + m_telop + '\n' \
          + '最高気温：' + m_max + '\n' \
          + '最低気温：' + m_min

logger.debug('Line送信開始')
logger.debug(m_title + ',' + m_date + ',' + m_telop + ',' + m_max + ',' + m_min)
linefunc.pushLine(LINE_URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE)
logger.debug('Line送信処理終了')
logger.info('天気取得処理終了')

