"""
Создание именованного логгера;
Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
Журналирование должно производиться в лог-файл;
На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.
"""

import logging
from logging.handlers import TimedRotatingFileHandler
import os
from Lesson_5_Logging.common.config import (
    SERVER_LOG_FILENAME,
    SERVER_LOGGER_NAME,
    FORMATTER_CONFIG,
    DATE_TIME_CONFIG
)

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, SERVER_LOG_FILENAME)

SERVER_LOGGER = logging.getLogger(SERVER_LOGGER_NAME)
SERVER_LOGGER.setLevel(logging.ERROR)

SERVER_FILE_HANDLER = TimedRotatingFileHandler(PATH, when='D', interval=1, encoding='utf-8')
SERVER_FILE_HANDLER.setLevel(logging.INFO)

SERVER_FORMATTER = logging.Formatter(FORMATTER_CONFIG, DATE_TIME_CONFIG)

SERVER_FILE_HANDLER.setFormatter(SERVER_FORMATTER)

SERVER_LOGGER.addHandler(SERVER_FILE_HANDLER)
SERVER_LOGGER.setLevel(logging.DEBUG)

if __name__ == '__main__':
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(SERVER_FORMATTER)
    SERVER_LOGGER.addHandler(console)
    SERVER_LOGGER.debug('Отладочная информация')
    SERVER_LOGGER.info('Информационное сообщение')
    SERVER_LOGGER.warning('Предупреждение')
    SERVER_LOGGER.error('Ошибка')
    SERVER_LOGGER.critical('Критическое сообщение')
