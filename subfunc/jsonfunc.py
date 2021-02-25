import requests

WEATHER_URL = 'https://www.jma.go.jp/bosai/forecast/data/forecast/110000.json'
DATE_MODE = 1
AREA_MODE = 1

def getWeather(url):
    response = requests.get(url).json()
    return response

TRAIN_URL='https://tetsudo.rti-giken.jp/free/delay.json'
TRAIN_ROUTE = '武蔵野線'

def getTrainDelay(url):
    response = requests.get(url).json()
    return response


