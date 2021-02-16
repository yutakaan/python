import requests

WEATHER_URL = 'http://weather.livedoor.com/forecast/webservice/json/v1'
SITE_ID = '110010'

def getWeather(url, site_id):
    payload = {'city': site_id}
    response = requests.get(url, params=payload).json()
    return response

TRAIN_URL='https://tetsudo.rti-giken.jp/free/delay.json'
# 路線名を記載
TRAIN_ROUTE = ''

def getTrainDelay(url):
    response = requests.get(url).json()
    return response


