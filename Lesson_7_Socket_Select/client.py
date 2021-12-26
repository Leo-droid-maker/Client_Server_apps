"""
клиент отправляет запрос серверу;
сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде отдельных скриптов,
содержащих соответствующие функции.
Функции клиента: сформировать presence-сообщение; отправить сообщение серверу;
получить ответ сервера; разобрать сообщение сервера; параметры командной строки скрипта
client.py <addr> [<port>]: addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.

Реализовать применение созданных логгеров для решения двух задач:
Журналирование обработки исключений try/except. Вместо функции print() использовать журналирование и
обеспечить вывод служебных сообщений в лог-файл;
Журналирование функций, исполняемых на серверной и клиентской сторонах при работе мессенджера.
"""

import logging
from sys import argv, exit
import json
from common.config import (
    ACTION,
    PRESENCE,
    TIME,
    USER,
    ACCOUNT_NAME,
    RESPONSE,
    ERROR,
    MESSAGE,
    MESSAGE_TEXT,
    CLIENT_ARGS_ERROR,
    DEFAULT_PORT,
    DEFAULT_IP_ADDRESS,
    DEFAULT_CLIENT_MODE,
    SENDER,
)
from common.utils import get_data, send_data
from socket import socket, AF_INET, SOCK_STREAM
import time
from log import client_log_config
from decorators import my_log


LOGGER = logging.getLogger('client')
USER_NAME = 'Leo'

@my_log
def create_message_to_server(client_socket, account_name=USER_NAME):

    message = input('Введите сообщение для отправки или \'quit\' для завершения работы: ')
    if message == 'quit':
        client_socket.close()
        LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        exit(0)
    message_obj = {
        ACTION: MESSAGE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        },
        MESSAGE_TEXT: message
    }
    LOGGER.debug(f'Сформирован словарь сообщения: {message_obj}')
    return message_obj

@my_log
def create_presence_message_to_server(action=PRESENCE, account_name=USER_NAME):
    msg = {
        ACTION: action,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        },
    }
    if msg[ACTION] == PRESENCE and msg[USER][ACCOUNT_NAME] == USER_NAME:
        LOGGER.info(f'Сообщение создано: {msg}')
        return msg
    LOGGER.error(f"Ошибка: Неправильно указан тип сообщения {msg}")
    raise ValueError()

@my_log
def create_answer(response_obj):
    match response_obj[RESPONSE]:
        case 200:
            LOGGER.info('Ответ сервера - 200: OK')
            return '200: OK'
        case 400:
            LOGGER.error('Ответ сервера - 400: Bad request')
            return f'400: {response_obj[ERROR]}'
        case _:
            LOGGER.error("Неизвестная ошибка")
            raise ValueError()

@my_log
def get_message_from_server(message):
    match message[ACTION], message[SENDER], message[MESSAGE_TEXT]:
        case 'message', _, _:
            print(f'Получено сообщение от пользователя '
                  f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            LOGGER.info(f'Получено сообщение от пользователя '
                        f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        case _:
            LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


    # if ACTION in message and message[ACTION] == MESSAGE and \
    #         SENDER in message and MESSAGE_TEXT in message:
    #     print(f'Получено сообщение от пользователя '
    #           f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    #     LOGGER.info(f'Получено сообщение от пользователя '
    #                 f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    # else:
    #     LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')

def start_client():
    try:
        match argv:
            case (_, s_address, s_port_number, _, mode) if (65535 > int(s_port_number) > 1024) and (
                        len(s_address.split('.')) == 4) and mode in ('listen', 'send'):
                server_address = s_address
                server_port = int(s_port_number)
                client_mode = mode
                LOGGER.info(f'\nАдрес сервера: {server_address}\nПорт сервера: {server_port}\nРежим: {client_mode}')
            case _:
                LOGGER.critical(CLIENT_ARGS_ERROR)
                raise Exception(f'\n{CLIENT_ARGS_ERROR}')
    except ValueError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        client_mode = DEFAULT_CLIENT_MODE
        LOGGER.error(f'ОШИБКА! {CLIENT_ARGS_ERROR} \nБыли применены значения по умолчанию:\n'
              f'Адрес сервера: {server_address}\nАдрес порта: {server_port}\nРежим: {client_mode}')

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_address, server_port))

    presence_msg_to_server = create_presence_message_to_server()
    send_data(presence_msg_to_server, client_socket)

    response_from_server = get_data(client_socket)
    answer = create_answer(response_from_server)
    LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')


    # try:
    #     client_socket = socket(AF_INET, SOCK_STREAM)
    #     client_socket.connect((server_address, server_port))
    #
    #     presence_msg_to_server = create_presence_message_to_server()
    #     send_data(presence_msg_to_server, client_socket)
    #
    #     response_from_server = get_data(client_socket)
    #     print(answer := create_answer(response_from_server))
    #     LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
    # except json.JSONDecodeError:
    #     LOGGER.error('Не удалось декодировать полученную Json строку.')
    #     exit(1)
    # except ConnectionRefusedError:
    #     LOGGER.critical(
    #         f'Не удалось подключиться к серверу {server_address}:{server_port}, '
    #         f'конечный компьютер отверг запрос на подключение.')

    while True:
        match client_mode:
            case 'send':
                try:
                    send_data(create_message_to_server(client_socket), client_socket)
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    exit(1)
            case 'listen':
                try:
                    get_message_from_server(get_data(client_socket))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    exit(1)


        # client_socket.close()


if __name__ == '__main__':
    start_client()
