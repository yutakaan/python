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
from subfunc import slackfunc
from subfunc import logfunc
from subfunc import jsonfunc
from subfunc import extractdatafunc
from subfunc import exportcsvfunc

# set log
LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'getPredSolarRadiation.log')
logger = logfunc.get_logger(__name__, LOG_TXT)
# set line func
HEADER_MESSAGE = datetime.today().strftime("%Y/%m/%d %H:%M:%S") + ' 取得' + '\n'
TITLE = 'Get Prediction Solar Radiation.'
TOKEN = slackfunc.TOKEN
CHANNEL = slackfunc.CHANNEL
# set file info
FILE_PATH = os.path.expanduser('~') + '/python/data/'
FILE_NAME = datetime.today().strftime("%Y%m%d") + '_ndata.csv'
FILE_FULLPATH = FILE_PATH + FILE_NAME
COEFFICIENT_FILE_NAME = 'coefficientSolorRadiationInfo.csv'
COEFFICIENT_FILE_FULLPATH = FILE_PATH + COEFFICIENT_FILE_NAME
TARGET_MONTH = (datetime.today()-timedelta(1)).strftime("%m")
# set OutputImage info
IMAGE_FILE = datetime.today().strftime("%Y%m%d") + '_getPredSolarRadiation.png'
GEN_IMAGE_FILE = datetime.today().strftime("%Y%m%d") + '_getPredGenerationValue.png'
# set location info
LATITUDE = '35.8'    # 緯度
LONGITUDE = '139.75' # 経度
# set panel info
PCON_CAPACITY = 5.5
PANEL_CAPACITY = 6.39
ONE_PANEL_AREA = 1.03 * 1.673 # 面積
MAX_OUTPUT = 0.355 # 公称最大出力(kWh/枚)
ALL_PANEL_AREA = PANEL_CAPACITY / MAX_OUTPUT * ONE_PANEL_AREA # パネル全体の面積
CONV_EFFECIENCY = 0.206 # 変換効率

def main():
    logger.info('start getPredSolarRadiation.py')
    #logger.debug('Start Get Solar Radiation')
    # 緯度・経度から予測日射量を取得
    result_list = extractdatafunc.extractFile2KeyRowList(FILE_FULLPATH, LATITUDE, 0, LONGITUDE, 1, ',')
    # 方位角・傾斜角係数取得
    coefficient_list = extractdatafunc.extractFile1KeyRowList(COEFFICIENT_FILE_FULLPATH, TARGET_MONTH, 0, ',')
    time_list = []
    for i in range(24):
        time_list.append(str(i).zfill(2) + ':00')
    # 翌日分のみを抽出しDataFrameに変換
    df_result = pd.DataFrame({'time':time_list})
    df_result['horizontalvalue'] = list(np.array(result_list[17:41], dtype="float"))
    df_result['coefficient'] = list(np.array(coefficient_list[1:25], dtype="float"))
    # MJ -> kWh
    df_result['horizontalvalue'] = df_result['horizontalvalue'] * 0.278
    df_result['predSolarRadiation'] = df_result['horizontalvalue'] * df_result['coefficient']
    df_result['panelGenerationValue'] = df_result['predSolarRadiation'] * ALL_PANEL_AREA * CONV_EFFECIENCY
    df_result['pconGenerationValue'] = df_result['predSolarRadiation'] * PCON_CAPACITY
    df_result['predGenerationValue'] = df_result['panelGenerationValue'].where(\
                                           df_result['panelGenerationValue'] <= PCON_CAPACITY, \
                                           PCON_CAPACITY)
    index = df_result['predSolarRadiation'].idxmax()
    peak_time = str(df_result['time'][index])
    peak_value = str(round(df_result['predSolarRadiation'][index], 3))
    #logger.debug('peak_time = ' + peak_time + ', peak_value = ' + peak_value)
    gen_index = df_result['predGenerationValue'].idxmax()
    gen_peak_time = str(df_result['time'][gen_index])
    gen_peak_value = str(round(df_result['predGenerationValue'][gen_index], 3))
    #logger.debug('peak_time = ' + gen_peak_time + ', peak_value = ' + gen_peak_value)
    #logger.debug('End Get Solar Radiation')
    # 予測日射量のデータ整理
    # グラフをファイルに落とす
    #logger.debug('Start Create Pred Image')
    df_result.plot(x='time', y=['horizontalvalue', 'predSolarRadiation'])
    plt.xlabel("time")
    plt.ylabel("Solar Radiation [kWh/m2]")
    plt.savefig(FILE_PATH + IMAGE_FILE)
    #logger.debug('End Create Pred Image')
    # Lineに画像を送信
    LINE_MESSAGE = HEADER_MESSAGE + '\n' \
                    + '明日の予測日射量は以下です。' + '\n' \
                    + '・最大日射量：' + peak_value + '[kWh/m2]' + '\n' \
                    + '・時刻：' + peak_time
    #linefunc.pushPicture(LINE_URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE, FILE_PATH + IMAGE_FILE)
    slackfunc.postSlackTextWithPicture(TOKEN, CHANNEL, TITLE, LINE_MESSAGE, FILE_PATH + IMAGE_FILE)
    # グラフをファイルに落とす
    #logger.debug('Start Creat Generation Image')
    df_result.plot.bar(x='time', y='predGenerationValue', width=1)
    plt.xlabel("time")
    plt.ylabel("Pred Generation Value [kWh]")
    plt.savefig(FILE_PATH + GEN_IMAGE_FILE)
    #logger.debug('End Create Generation Image')
    # Lineに画像を送信
    LINE_MESSAGE = '明日の予測発電量は以下です。' + '\n' \
                     + '・最大発電量：' + gen_peak_value + '[kWh]' + '\n' \
                     + '・時刻：' + gen_peak_time
    #linefunc.pushPicture(LINE_URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE, FILE_PATH + GEN_IMAGE_FILE)
    slackfunc.postSlackTextWithPicture(TOKEN, CHANNEL, TITLE, LINE_MESSAGE, FILE_PATH + GEN_IMAGE_FILE)
    logger.info('end getPredSolarRadiation.py')

if __name__=='__main__':
    main()
