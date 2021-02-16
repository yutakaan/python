import os
import logging
import logging.config

log_dir = os.path.expanduser('~') + '/python/log'

# set logger
def get_logger(logger_name,log_file):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = '%(asctime)s : %(levelname)s : %(message)s'
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(stream_handler)
    #file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1000000, backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(file_handler)

    return logger

