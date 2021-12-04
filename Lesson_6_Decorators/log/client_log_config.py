"""
Создание именованного логгера;
Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
Журналирование должно производиться в лог-файл;
"""

import logging
import sys, os
sys.path.append("..")

from Lesson_6_Decorators.common.config import (
    CLIENT_LOG_FILENAME,
    CLIENT_LOGGER_NAME,
    FORMATTER_CONFIG,
    DATE_TIME_CONFIG
)

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, CLIENT_LOG_FILENAME)

CLIENT_LOGGER = logging.getLogger(CLIENT_LOGGER_NAME)
CLIENT_LOGGER.setLevel(logging.ERROR)

CLIENT_FILE_HANDLER = logging.FileHandler(PATH)
# CLIENT_FILE_HANDLER.setLevel(logging.INFO)

CLIENT_FORMATTER = logging.Formatter(FORMATTER_CONFIG, DATE_TIME_CONFIG)

CLIENT_FILE_HANDLER.setFormatter(CLIENT_FORMATTER)

CLIENT_LOGGER.addHandler(CLIENT_FILE_HANDLER)
CLIENT_LOGGER.setLevel(logging.DEBUG)

if __name__ == '__main__':
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(CLIENT_FORMATTER)
    CLIENT_LOGGER.addHandler(console)
    CLIENT_LOGGER.debug('Отладочная информация')
    CLIENT_LOGGER.info('Информационное сообщение')
    CLIENT_LOGGER.warning('Предупреждение')
    CLIENT_LOGGER.error('Ошибка')
    CLIENT_LOGGER.critical('Критическое сообщение')
