import requests
import os
import sys
from subfunc import logfunc
from subfunc import jsonfunc
from subfunc import linefunc
from subfunc import token

# logger設定
LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'trainDelay.log')

# API情報取得
URL = jsonfunc.TRAIN_URL
if(len(sys.argv) == 1 ):
    ROUTE = jsonfunc.TRAIN_ROUTE
else:
    ROUTE = sys.argv[1]

# LINE設定
LINE_URL = linefunc.URL
ACCESS_TOKEN = token.ACCESS_TOKEN
HEADERS = linefunc.HEADERS

logger = logfunc.get_logger(__name__, LOG_TXT)

def searchTargetLine(delay_data,ROUTE):
    flag = 0
    i = 0
    for name in range(len(delay_data)):
        DELAY_ROUTE = delay_data[i]['name']
        if(DELAY_ROUTE==ROUTE):
            LINE_MESSAGE = DELAY_ROUTE + 'は遅延しています。'
            flag = 1
            break;
        i = i + 1

    if(flag==0):
        LINE_MESSAGE = ROUTE + 'の遅延情報はありません。'
  
    return LINE_MESSAGE

def main():

    # API取得処理
    logger.debug('API実行')
    delay_data = jsonfunc.getTrainDelay(URL)
    logger.debug('API終了')
    # 対象の路線を検索
    LINE_MESSAGE = searchTargetLine(delay_data,ROUTE)
    # LINE通知
    logger.debug('LINE送信処理開始')
    logger.debug(LINE_MESSAGE)
    linefunc.pushLine(LINE_URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE)
    logger.debug('LINE送信処理終了')

if __name__ == "__main__":
    logger.info('鉄道遅延情報取得開始')
    main()
    logger.info('鉄道遅延情報取得取得終了')
