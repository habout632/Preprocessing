__author__ = 'x-man,habout'

import logging
import logzero
import os
import time
from logzero import logger

# print(os.getcwd())
# os.chmod("/var/log", 755)
logzero.logfile("/tmp/recommender"+(time.strftime("%Y-%m-%d", time.localtime()))+".log", maxBytes=10000000, backupCount=10)
formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
logzero.formatter(formatter)


class Log:
    @staticmethod
    def debug(msg):
       logger.debug(msg)

    @staticmethod
    def info(msg):
       logger.info(msg)

    @staticmethod
    def warning(msg):
       logger.warning(msg)

    @staticmethod
    def error(msg):
            logger.error(msg)

# Log.error("出错了出错了出错了出错了出错了出错了1111")
