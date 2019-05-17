import os
import time
from enum import Enum

import logging

cur_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path):
    os.mkdir(log_path)


class LogHelperType(Enum):
    FATAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


class LogHelper:
    def __init__(self):
        # 文件的命名
        self.logname = os.path.join(log_path, '%s.log' % time.strftime('%Y_%m_%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')

    def __console(self, level: LogHelperType, message):
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')  # 这个是python3的
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == LogHelperType.DEBUG:
            self.logger.debug(message)
        elif level == LogHelperType.INFO:
            self.logger.info(message)
        elif level == LogHelperType.WARNING:
            self.logger.warning(message)
        elif level == LogHelperType.ERROR:
            self.logger.error(message)
        elif level == LogHelperType.FATAL:
            self.logger.fatal(message)

        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console(LogHelperType.DEBUG, message)

    def info(self, message):
        self.__console(LogHelperType.INFO, message)

    def warning(self, message):
        self.__console(LogHelperType.WARNING, message)

    def error(self, message):
        self.__console(LogHelperType.ERROR, message)

    def fatal(self, message):
        self.__console(LogHelperType.FATAL, message)
