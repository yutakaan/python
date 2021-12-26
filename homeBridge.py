import requests
import os
import sys
import json
from subfunc import logfunc
from subfunc import linefunc
from subfunc import env
from subfunc import token
import subprocess
import shlex

# logger設定
LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'homeBridge.log')
logger = logfunc.get_logger(__name__, LOG_TXT)

# LINE設定
LINE_URL = linefunc.URL
ACCESS_TOKEN = token.ACCESS_TOKEN
HEADERS = linefunc.HEADERS

# config.json
FILE = os.path.expanduser('~') + '/.homebridge/config.json'

# IRKIT IP
IP = env.IRKIT_IP
cmd_curl = 'curl -i "http://' + IP + '/messages" -H "X-Requested-With: curl" -d '

ACCESSORY = sys.argv[1]
MODE = sys.argv[2]

def readConfig(file, accessory, on_off_type):

    flag = 0
    json_file = json.load(open(file, 'r'))
    for i in range(len(json_file['accessories'])):
        name = json_file['accessories'][i]['name']
        if(accessory==name):
            raw = json_file['accessories'][i][on_off_type]
            flag = 1
            break;
        else:
            flag = 0
            raw = 0

    return flag, raw

def main():
    if MODE=='1':
        on_off_type = 'on_form'
    elif MODE=='0':
        on_off_type = 'off_form'
    else:
        logger.error('モードが違います。')
        logger.info('homeBridge終了')
        exit()

    flag, raw = readConfig(FILE, ACCESSORY, on_off_type)
    if flag==0:
        logger.error('アクセサリが存在しません。')
    else:
        cmd_exec = cmd_curl + '\'' + str(raw).replace('\'', '"') + '\''
        subprocess.run(shlex.split(cmd_exec))
        #print(cmd_exec)

if __name__ == "__main__":
    logger.info('homeBridge開始')
    main()
    logger.info('homeBridge終了')
