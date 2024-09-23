from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os
import sys
import logging
import time

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)

logger_initialized = {}
LOG_FORMAT = "[%(asctime)s] %(levelname)s %(name)s %(filename)s [line:%(lineno)d]: %(message)s"

def get_logger(name=None,log_file="./log/log.log", log_level=logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    if name in logger_initialized:
        return logger
    formatter = logging.Formatter(LOG_FORMAT,datefmt="%Y/%m/%d %H:%M:%S")
    #控制台日志输出
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    #文件日志输出
    if log_file is not None:
        log_file_folder = os.path.split(log_file)[0]
        os.makedirs(log_file_folder, exist_ok=True)
        tfh = TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=3, encoding='UTF-8', delay=False, utc=False, atTime=time)
        tfh.setFormatter(formatter)
        logger.addHandler(tfh)
    logger.setLevel(log_level)
    logger_initialized[name] = True
    logger.propagate = False
    return logger
 