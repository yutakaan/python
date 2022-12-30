import requests
from bs4 import BeautifulSoup
import json

WEATHER_URL = 'https://www.jma.go.jp/bosai/forecast/data/forecast/110000.json'
DATE_MODE = 1
AREA_MODE = 1

def getWeather(url):
    response = requests.get(url).json()
    return response

TRAIN_URL='https://rti-giken.jp/fhc/api/train_tetsudo/'
TRAIN_ROUTE = '武蔵野線'

def getTrainDelay(url):
    html = requests.get(url)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'html.parser')
    response = json.loads(soup.find_all('div')[2].get_text())
    return response


