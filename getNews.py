# coding: utf-8
import requests
from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import os
import sys
from subfunc import linefunc
from subfunc import token
from subfunc import logfunc

# set LINE
LINE_URL = linefunc.URL
ACCESS_TOKEN = token.ACCESS_TOKEN
HEADERS = linefunc.HEADERS

# set log
LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'getNews.log')
logger = logfunc.get_logger(__name__, LOG_TXT)

LINE_MESSAGE = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' 取得'
TIME_HH = datetime.datetime.now().strftime("%H")

SEND_FLAG=sys.argv[1]

def getNews():
    URL = 'https://www.yahoo.co.jp/'
    html = requests.get(URL)
    html.encoding = 'utf-8'
    logger.debug('get news')
    soup = BeautifulSoup(html.text, 'html.parser')
    KEYWORD = 'news.yahoo.co.jp/pickup'
    titles = LINE_MESSAGE + '\n'

    newslist = soup.find_all(href=re.compile(KEYWORD))
    for i in range(len(newslist)):
        title = newslist[i].find('span').get_text()
        logger.debug('contents:' + title)
        titles = titles +  '\n' + '・' + title

    return titles

def main():
    logger.info('処理開始')
    contents = getNews()
    if SEND_FLAG == '1':
        linefunc.pushLine(LINE_URL, ACCESS_TOKEN, HEADERS, contents)
    logger.info('処理終了')

if __name__=='__main__':
    main()
