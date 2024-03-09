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
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from beautifultable import BeautifulTable
from subfunc import linefunc
from subfunc import token
from subfunc import logfunc
from subfunc import jsonfunc
from subfunc import extractdatafunc
from subfunc import exportcsvfunc

# set log
LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'powerGenerationTransition.log')
logger = logfunc.get_logger(__name__, LOG_TXT)
# set line func
LINE_URL = linefunc.URL
ACCESS_TOKEN = token.ACCESS_TOKEN
HEADERS = linefunc.HEADERS
HEADER_MESSAGE = datetime.today().strftime("%Y/%m/%d %H:%M:%S") + ' 取得' + '\n'
# set file info
FILE_PATH = os.path.expanduser('~') + '/python/data/'
FILE_NAME = 'SimulationGenInfo.csv'
FILE_FULLPATH = FILE_PATH + FILE_NAME
# set Generator Info
PERIOD_YEAR = 20      # 予測期間（年）
MIN_DET_RATE = 0.005  # 最小劣化率
MAX_DET_RATE = 0.01   # 最大劣化率
PANEL_CAPACITY = 6.39 # 太陽光パネルの容量kW
PCON_CAPACITY = 5.5   # パワーコンディショナーの容量kW
d_start_date = datetime(2022, 8, 1)
d_end_date = datetime.today()-dateutil.relativedelta.relativedelta(months=1)
MEAN_VALUE = 12       # 移動平均に使う値
# set OutputImage info
IMAGE_FILE = datetime.today().strftime("%Y%m%d") + '_powerGenerationTransition.png'
# set URL
MONTHLY_VALUE_URL = jsonfunc.MONTHLY_VALUE_URL

# 発電量取得
def getGenValue(URL, TARGET_DATE):
    result = jsonfunc.getResultEnergyValue(URL, TARGET_DATE)

    return result

# 劣化率を考慮した発電量の計算
def calcDetGenVal(month, det_rate, panel_capacity, pcon_capacity):
    capacity = min(panel_capacity, pcon_capacity)
    loss_gen = (month-1)*det_rate/12
    detGenValue = capacity*(1-loss_gen)

    return detGenValue

def main():
    logger.info('処理開始')
    diff_period = dateutil.relativedelta.relativedelta(d_end_date, d_start_date)
    diff_months = diff_period.years*12+diff_period.months+1
    df_result = pd.DataFrame()
    # 各月毎の値を算出
    logger.debug('Start Calc Generation')
    for i in range(diff_months):
        # 発電量取得
        target_date = (d_start_date + dateutil.relativedelta.relativedelta(months=i)).strftime("%Y%m%d")
        genValue = (getGenValue(MONTHLY_VALUE_URL, target_date))[0]
        # 対象月の発電シミュレーション値取得
        simGenValue = float(extractdatafunc.extractFile2DCol(FILE_FULLPATH, target_date[4:6], 0, 2, ','))
        # 劣化率を考慮したシミュレーション値
        min_det_genValue = calcDetGenVal(i, MIN_DET_RATE, PANEL_CAPACITY, PCON_CAPACITY) * simGenValue
        max_det_genValue = calcDetGenVal(i, MAX_DET_RATE, PANEL_CAPACITY, PCON_CAPACITY) * simGenValue
        # データ格納
        result_list = [[i+1, target_date[0:6], genValue, min_det_genValue, max_det_genValue]]
        df = pd.DataFrame(result_list, columns=['index', 'month', 'genValue', \
                'minDetValue', 'maxDetValue'])
        df_result = pd.concat([df_result, df])
    logger.debug('End Calc Generation')
    # 移動平均の算出
    logger.debug('Start Calc MovingAverage')
    df_mean = pd.concat([df_result.loc[:, ['index', 'month']], \
            df_result.loc[:, ['genValue', 'minDetValue', 'maxDetValue']].rolling(MEAN_VALUE).mean()], \
            axis=1).dropna(how='any')
    logger.debug('End Calc Moving Average')
    # グラフをファイルに落とす
    logger.debug('Start Create Image')
    df_mean.plot(x='index', y=['genValue', 'minDetValue', 'maxDetValue'])
    plt.xlabel("months")
    plt.ylabel("Power Generation (kWh)")
    plt.savefig(FILE_PATH + IMAGE_FILE)
    logger.debug('End Create Image')
    # Lineに画像を送信
    LINE_MESSAGE = HEADER_MESSAGE
    linefunc.pushPicture(LINE_URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE, FILE_PATH + IMAGE_FILE)
    logger.info('処理終了')

if __name__=='__main__':
    main()
