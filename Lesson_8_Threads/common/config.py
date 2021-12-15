"""Константы"""

# Порт по умолчанию
DEFAULT_PORT = 7777
# IP- адрес по умолчанию
DEFAULT_IP_ADDRESS = '127.0.0.1'

MAX_CONNECTIONS = 5
# Максимальная длина сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# КОдировка проекта
ENCODING = 'utf-8'

DEFAULT_CLIENT_MODE = 'listen'
DEFAULT_CLIENT_NAME = None


# Протокол JIM остновные ключи
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
TYPE ='type'
STATUS = 'status'
DESTINATION = 'to'

# Прочие ключи протокола JIM
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'


# Ошибки
SERVER_ARGS_ERROR = '\nВведите параметры в следующем порядке: <имя файла> -p <номер порта> -a <IP адрес>\n'

CLIENT_ARGS_ERROR = 'Возможно, неправиьно указан один из параметров\n' \
                    'Введите параметры в следующем порядке: <имя файла> <IP адрес сервера> <номер порта сервера>'

# Настройки логирования
CLIENT_LOG_FILENAME = 'client.logs'
CLIENT_LOGGER_NAME = 'client'

SERVER_LOG_FILENAME = 'server.logs'
SERVER_LOGGER_NAME = 'server'

FORMATTER_CONFIG = "%(asctime)s; %(levelname)s; %(filename)s; %(message)s"
DATE_TIME_CONFIG = "%Y-%m-%d %H:%M:%S"
