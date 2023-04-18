# coding: utf-8
import requests
from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime, date, timedelta
import os
import sys
from subfunc import linefunc
from subfunc import token
from subfunc import logfunc
from subfunc import jsonfunc
from subfunc import extractdatafunc

# set log
LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'calcEnergyPrice.log')
logger = logfunc.get_logger(__name__, LOG_TXT)
# set line func
LINE_URL = linefunc.URL
ACCESS_TOKEN = token.ACCESS_TOKEN
HEADERS = linefunc.HEADERS
HEADER_MESSAGE = datetime.today().strftime("%Y/%m/%d %H:%M:%S") + ' 取得' + '\n'
TIME_HH = datetime.today().strftime("%H")

ENERGY_PRICE_FILE=os.path.expanduser('~') + '/python/data/energyPrice.csv'
TARGET_DATE = (datetime.today()-timedelta(1)).strftime("%Y%m%d")
ENERGY_TIME_VALUE_URL = jsonfunc.ENERGY_TIME_VALUE_URL
GENERATOR_VALUE_URL = jsonfunc.GENERATOR_VALUE_URL
DIVTYPE = ','

def calcDailyPrice(TARGET_DATE):
    # 時間帯別使用量取得
    totalA, totalB, totalC, totalD = jsonfunc.getEnergyTimeValue(ENERGY_TIME_VALUE_URL, TARGET_DATE)
    logger.debug('totalA = ' + str(totalA) \
                 + ' totalB = ' + str(totalB) \
                 + ' totalC = ' + str(totalC) \
                 + ' totalD = ' + str(totalD))
    # 単価取得
    basePrice = extractdatafunc.extractFile2DCol(ENERGY_PRICE_FILE, 'BASEPRICE', 0, 1, DIVTYPE)
    basePriceTitle = extractdatafunc.extractFile2DCol(ENERGY_PRICE_FILE, 'BASEPRICE', 0, 1, DIVTYPE)
    priceA = extractdatafunc.extractFile2DCol(ENERGY_PRICE_FILE, 'PRICEA', 0, 1, DIVTYPE)
    priceATitle = extractdatafunc.extractFile2DCol(ENERGY_PRICE_FILE, 'PRICEA', 0, 2, DIVTYPE)
    priceB = extractdatafunc.extractFile2DCol(ENERGY_PRICE_FILE, 'PRICEB', 0, 1, DIVTYPE)
    priceBTitle = extractdatafunc.extractFile2DCol(ENERGY_PRICE_FILE, 'PRICEB', 0, 2, DIVTYPE)
    priceC = extractdatafunc.extractFile2DCol(ENERGY_PRICE_FILE, 'PRICEC', 0, 1, DIVTYPE)
    priceCTitle = extractdatafunc.extractFile2DCol(ENERGY_PRICE_FILE, 'PRICEC', 0, 2, DIVTYPE)
    priceD = extractdatafunc.extractFile2DCol(ENERGY_PRICE_FILE, 'PRICED', 0, 1, DIVTYPE)
    priceDTitle = extractdatafunc.extractFile2DCol(ENERGY_PRICE_FILE, 'PRICED', 0, 2, DIVTYPE)
    reEnePrice = extractdatafunc.extractFile2DCol(ENERGY_PRICE_FILE, 'REENEPRICE', 0, 1, DIVTYPE)
    fuelPrice = extractdatafunc.extractFile2DCol(ENERGY_PRICE_FILE, 'FUELPRICE', 0, 1, DIVTYPE)
    # 発電消費実績取得
    totalGeneration, totalConsumption, totalSelling, totalBuying \
            = jsonfunc.getResultEnergyValue(GENERATOR_VALUE_URL, TARGET_DATE)
    logger.debug('totalGeneration = ' + str(totalGeneration) \
                 + ' totalConsumption = ' + str(totalConsumption) \
                 + ' totalSelling = ' + str(totalSelling) \
                 + ' totalBuying = ' + str(totalBuying))
    # 電気料金計算
    energyPrice = float(basePrice) / 30 \
                  + float(priceA) * float(totalA - (totalConsumption - totalBuying)) \
                  + float(priceB) * float(totalB) \
                  + float(priceC) * float(totalC) \
                  + float(priceD) * float(totalD) \
                  + float(reEnePrice) * totalBuying \
                  + float(fuelPrice) * totalBuying
    energyPrice = round(energyPrice, 3)
    logger.debug('energyPrice = ' + str(energyPrice))
    contents =  '■実績' + '\n'  \
                + '・発電量：' + str(totalGeneration) + 'kWh' + '\n' \
                + '・消費量：' + str(totalConsumption) + 'kWh' + '\n' \
                + '・売電量：' + str(totalSelling) + 'kWh' + '\n' \
                + '・買電量：' + str(totalBuying) + 'kWh' + '\n' \
                + '■使用量内訳' + '\n' \
                + '・' + priceATitle + '：' + str(totalA) + 'kWh' + '\n' \
                + '・' + priceBTitle + '：' + str(totalB) + 'kWh' + '\n' \
                + '■電気料金の目安' + '\n' \
                +  str(energyPrice) + '円' +'\n' \
                + '※再エネ賦課金：' + str(reEnePrice) + '円/kWh' + '\n' \
                + '※燃料調整費：' + str(fuelPrice) + '円/kWh' 

    return contents

def main():
    logger.info('処理開始')
    TARGET_DATE = (datetime.today()-timedelta(1)).strftime("%Y/%m/%d")
    logger.debug('使用量計算処理開始')
    contents = calcDailyPrice(TARGET_DATE)
    logger.debug('使用量計算処理終了')
    LINE_MESSAGE = HEADER_MESSAGE \
                   + TARGET_DATE + 'の電気使用量実績' + '\n' \
                   + contents
    linefunc.pushLine(LINE_URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE)
    logger.info('処理終了')

if __name__=='__main__':
    main()
