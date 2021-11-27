"""Константы"""

# Порт по умолчанию
DEFAULT_PORT = 7777
# IP- адрес по умолчанию
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная длина сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# КОдировка проекта
ENCODING = 'utf-8'

# Протокол JIM остновные ключи
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
TYPE ='type'
STATUS = 'status'

# Прочие ключи протокола JIM
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
RESPONDEFAULT_IP_ADDRESS = 'respondefault_ip_address'


# Разное
SERVER_ARGS_ERROR = '\nВведите параметры в следующем порядке: <имя файла> -p <номер порта> -a <IP адрес>\n'

CLIENT_ARGS_ERROR = 'Возможно, неправиьно указан один из параметров\n' \
                    'Введите параметры в следующем порядке: <имя файла> <IP адрес сервера> <номер порта сервера>'
