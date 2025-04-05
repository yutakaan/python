import requests
import os
import sys
from subfunc import logfunc
from subfunc import jsonfunc
from subfunc import slackfunc

LINE_MESSAGE = sys.argv[1]

# set logger
LOG_DIR = logfunc.log_dir
LOG_TXT = os.path.join(LOG_DIR, 'pushAnyMessage.log')
logger = logfunc.get_logger(__name__, LOG_TXT)

# set line func
WEBHOOK_URL = slackfunc.WEBHOOK_URL
HEADERS = slackfunc.HEADERS
TITLE = 'Daily Message.'

def main():
    logger.info('start pushAnyMessage.py')
    logger.debug('message = ' + LINE_MESSAGE)
    #linefunc.pushLine(LINE_URL, ACCESS_TOKEN, HEADERS, LINE_MESSAGE)
    slackfunc.postSlackText(WEBHOOK_URL, HEADERS, TITLE, LINE_MESSAGE)
    logger.info('end pushAnyMessage.py')

if __name__=='__main__':
    main()
