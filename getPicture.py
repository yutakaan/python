# coding: utf-8
import sys
import os
import cv2
import time
import datetime
from subfunc import linefunc
from subfunc import logfunc

# set Picture
IMAGE_PATH = os.path.expanduser('~') + '/python/log/'
SEND_FLAG=sys.argv[1]
print(SEND_FLAG)
# set LINE
URL = linefunc.URL
ACCESS_TOKEN = linefunc.ACCESS_TOKEN
HEADERS = linefunc.HEADERS

# set log
LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'getPicture.log')
logger = logfunc.get_logger(__name__, LOG_TXT)

LINE_MESSAGE = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' 撮影'
TIME_HH = datetime.datetime.now().strftime("%H")
IMAGE_FILE = IMAGE_PATH + 'picture_' + TIME_HH + '.jpg'

# 写真を撮る
def getPicture(IMAGE_FILE):
    cc = cv2.VideoCapture(0)
    rr, img = cc.read()
    cv2.imwrite(IMAGE_FILE,img)
    cc.release()

# 指定した時間のみ写真を送る
def sendPicture(URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE, IMAGE_FILE):
    linefunc.pushPicture(URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE, IMAGE_FILE)
    logger.info('Send Picture to LINE.')

def main():
    logger.info('処理開始')
    getPicture(IMAGE_FILE)
    if SEND_FLAG == '1':
        sendPicture(URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE, IMAGE_FILE)
    logger.info('処理終了')

if __name__=='__main__':
    main()
