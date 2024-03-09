# coding: utf-8
import requests
from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime, date, timedelta
import dateutil.relativedelta
import os
import sys
import calendar
import numpy as np
from beautifultable import BeautifulTable
from subfunc import linefunc
from subfunc import token
from subfunc import logfunc
from subfunc import jsonfunc
from subfunc import extractdatafunc

# set log
LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'compareEnergy.log')
logger = logfunc.get_logger(__name__, LOG_TXT)
# set line func
LINE_URL = linefunc.URL
ACCESS_TOKEN = token.ACCESS_TOKEN
HEADERS = linefunc.HEADERS
HEADER_MESSAGE = datetime.today().strftime("%Y/%m/%d %H:%M:%S") + ' 取得' + '\n'
# set date data
t_date = datetime.today()-timedelta(1)
TARGET_DATE = t_date.strftime("%Y%m%d")
# set past date data
p_date = datetime.today()-dateutil.relativedelta.relativedelta(years=1)
PAST_TARGET_DATE = p_date.strftime("%Y%m%d")
PAST_DAYS_IN_MONTH = calendar.monthrange(p_date.year, p_date.month)[1]
# set URL
GENERATOR_VALUE_URL = jsonfunc.GENERATOR_VALUE_URL
MONTHLY_VALUE_URL = jsonfunc.MONTHLY_VALUE_URL

def getValue(URL, TARGET_DATE):
    # 発電消費実績取得
    result = jsonfunc.getResultEnergyValue(URL, TARGET_DATE)
    logger.debug('totalGeneration = ' + str(result[0]) \
                 + ' totalConsumption = ' + str(result[1]) \
                 + ' totalSelling = ' + str(result[2]) \
                 + ' totalBuying = ' + str(result[3]))

    return result

def main():
    logger.info('処理開始')
    logger.debug('前日発電消費量取得開始')
    nowDailyResult = list(getValue(GENERATOR_VALUE_URL, TARGET_DATE))
    logger.debug('前日発電消費量取得終了')
    logger.debug('前日までの累積発電消費量取得開始')
    nowMonResult = list(getValue(MONTHLY_VALUE_URL, TARGET_DATE))
    logger.debug('前日までの累積発電消費量取得処理終了')
    logger.debug('1年前発電消費量取得開始')
    pastMonResult = list(getValue(MONTHLY_VALUE_URL, PAST_TARGET_DATE))
    logger.debug('1年前発電消費量取得終了')
    logger.debug('同月1年前の平均発電消費量取得開始')
    pastDailyResult = []
    pastDailyResult = [round(pastMonResult[i]/PAST_DAYS_IN_MONTH, 1) for i in range(0, len(pastMonResult))]
    logger.debug('totalGeneration = ' + str(pastDailyResult[0]) \
                + ' totalConsumption = ' + str(pastDailyResult[1]) \
                + 'totalSelling = ' + str(pastDailyResult[2]) \
                + 'totalBuying = ' + str(pastDailyResult[3]))
    logger.debug('同月1年前の平均発電消費量取得終了')
    title_list = ["GEN", "USE", "SEL", "BUY"]
    data = np.array([nowDailyResult, pastDailyResult, nowMonResult, pastMonResult])
    table = BeautifulTable()
    table.columns.header = title_list
    for j in range(len(data)):
        table.rows.append(data[j])
    table.set_style(BeautifulTable.STYLE_COMPACT)
    LINE_MESSAGE = HEADER_MESSAGE + '\n' \
                   + str(table) + '\n' \
                   + '\n' \
                   + '1：前日の実績' + '\n' \
                   + '2：前年同月の1日平均' + '\n' \
                   + '3：前日までの累積' + '\n' \
                   + '4：前年同月1ヶ月の累積'
    linefunc.pushLine(LINE_URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE)
    logger.info('処理終了')

if __name__=='__main__':
    main()
