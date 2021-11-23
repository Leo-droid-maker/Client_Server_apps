"""
клиент отправляет запрос серверу;
сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде отдельных скриптов,
содержащих соответствующие функции.
Функции клиента: сформировать presence-сообщение; отправить сообщение серверу;
получить ответ сервера; разобрать сообщение сервера; параметры командной строки скрипта
client.py <addr> [<port>]: addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.
"""

from sys import argv
from config import *
from socket import socket, AF_INET, SOCK_STREAM
import time
import json

USER_NAME = 'Leo'


def create_presence_message_to_server(account_name=USER_NAME):
    msg = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        },
    }
    return msg


def create_answer(response_obj):
    match response_obj[RESPONSE]:
        case 200:
            return '200: OK'
        case _:
            raise ValueError(f'400: {response_obj[ERROR]}')


def send_message_to_server(message_obj, clnt_socket):
    js_msg = json.dumps(message_obj)
    encoded_msg = js_msg.encode(encoding=ENCODING)
    clnt_socket.send(encoded_msg)


def get_response_from_server(clnt_socket):
    response = clnt_socket.recv(MAX_PACKAGE_LENGTH)
    js_response = response.decode(encoding=ENCODING)
    decoded_response = json.loads(js_response)
    return decoded_response


def start_client():
    try:
        match argv:
            case (_, s_address, s_port_number) if (65535 > int(s_port_number) > 1024):
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
    send_message_to_server(msg_to_server, client_socket)

    response_from_server = get_response_from_server(client_socket)
    print(create_answer(response_from_server))

    client_socket.close()


start_client()
