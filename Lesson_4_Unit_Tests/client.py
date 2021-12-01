"""
клиент отправляет запрос серверу;
сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде отдельных скриптов,
содержащих соответствующие функции.
Функции клиента: сформировать presence-сообщение; отправить сообщение серверу;
получить ответ сервера; разобрать сообщение сервера; параметры командной строки скрипта
client.py <addr> [<port>]: addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.
"""

from sys import argv
from common.config import (
    ACTION,
    PRESENCE,
    TIME,
    USER,
    ACCOUNT_NAME,
    RESPONSE,
    ERROR,
    CLIENT_ARGS_ERROR,
    DEFAULT_PORT,
    DEFAULT_IP_ADDRESS
)
from common.utils import get_data, send_data
from socket import socket, AF_INET, SOCK_STREAM
import time

USER_NAME = 'Leo'


def create_presence_message_to_server(action=PRESENCE, account_name=USER_NAME):
    msg = {
        ACTION: action,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        },
    }
    if msg[ACTION] == PRESENCE and msg[USER][ACCOUNT_NAME] == USER_NAME:
        return msg
    raise ValueError


def create_answer(response_obj):
    match response_obj[RESPONSE]:
        case 200:
            return '200: OK'
        case 400:
            return f'400: {response_obj[ERROR]}'
        case _:
            raise ValueError("ERROR")


def start_client():
    try:
        match argv:
            case (_, s_address, s_port_number) if (65535 > int(s_port_number) > 1024) and (
                        len(s_address.split('.')) == 4):
                server_address = s_address
                server_port = int(s_port_number)
            case _:
                raise Exception(f'\n{CLIENT_ARGS_ERROR}')
    except ValueError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        print(f'ОШИБКА! {CLIENT_ARGS_ERROR} \nБыли применены значения по умолчанию:\n'
              f'Адрес сервера: {server_address}\nАдрес порта: {server_port}')

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_address, server_port))

    msg_to_server = create_presence_message_to_server()
    send_data(msg_to_server, client_socket)

    response_from_server = get_data(client_socket)
    print(create_answer(response_from_server))

    client_socket.close()


if __name__ == '__main__':
    start_client()
