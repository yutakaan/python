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

ENERGY_TIME_VALUE_URL='http://OMRON/asyncquery.cgi?type=Consume&subType=2&timeType=1'

def getEnergyTimeValue(url, target_date):
    target_yyyy = target_date[0:4]
    target_mm = target_date[4:6]
    target_dd = target_date[6:8]
    target_url = url + '&year=' + target_yyyy + '&month=' + target_mm + '&day=' + target_dd
    response = requests.get(target_url).json()
    totalA = round(int(response['totalConsumptionA'])*0.1, 3)
    totalB = round(int(response['totalConsumptionB'])*0.1, 3)
    totalC = round(int(response['totalConsumptionC'])*0.1, 3)
    totalD = round(int(response['totalConsumptionD'])*0.1, 3)
    return totalA, totalB, totalC, totalD

GENERATOR_VALUE_URL = 'http://OMRON/asyncquery.cgi?type=Record&timeType=1'
MONTHLY_VALUE_URL = 'http://OMRON/asyncquery.cgi?type=Record&timeType=2'

def getResultEnergyValue(url, target_date):
    target_yyyy = target_date[0:4]
    target_mm = target_date[4:6]
    target_dd = target_date[6:8]
    target_url = url + '&year=' + target_yyyy + '&month=' + target_mm + '&day=' + target_dd
    response = requests.get(target_url).json()
    totalGeneration = round(int(response['totalGeneration'])*0.1, 3)
    totalConsumption = round(int(response['totalConsumption'])*0.1, 3)
    totalSelling = round(int(response['totalSelling'])*0.1 ,3)
    totalBuying = round(int(response['totalBuying'])*0.1 ,3)

    return totalGeneration, totalConsumption, totalSelling, totalBuying

