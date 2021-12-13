"""
клиент отправляет запрос серверу;
сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде отдельных скриптов,
содержащих соответствующие функции.
Функции сервера: принимает сообщение клиента; формирует ответ клиенту; отправляет ответ клиенту;
имеет параметры командной строки: -p <port> — TCP-порт для работы (по умолчанию использует 7777); -a <addr> —
IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).

Реализовать применение созданных логгеров для решения двух задач:
Журналирование обработки исключений try/except. Вместо функции print() использовать журналирование и
 обеспечить вывод служебных сообщений в лог-файл;
Журналирование функций, исполняемых на серверной и клиентской сторонах при работе мессенджера.
"""

import json
import logging
import log.server_log_config
from sys import argv
from common.config import *
from common.utils import get_data, send_data
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

SERVER_LOGGER = logging.getLogger('server')


def create_response(message):
    match message[ACTION], message[TIME], message[USER][ACCOUNT_NAME]:
        case 'presence', _, 'Leo':
            SERVER_LOGGER.info('Ответ сервера - 200: OK')
            return {RESPONSE: 200}
        case None, None, None:
            SERVER_LOGGER.error(f"Ошибка: Неправильно указан тип сообщения {message}")
            raise ValueError
        case _:
            SERVER_LOGGER.error('Ответ сервера - 400: Bad request')
            return {
                RESPONSE: 400,
                ERROR: "Bad request"
            }


def start_server():
    try:
        match argv:
            case (_, p, port_number, a, address) \
                if p == '-p' \
                   and a == '-a' \
                   and (65535 > int(port_number) > 1024) \
                   and (len(address.split('.')) == 4):
                listen_port = int(port_number)
                listen_address = address
                SERVER_LOGGER.info(f'\nПрослушивается: {listen_address}\nПорт: {listen_port}')
            case _:
                SERVER_LOGGER.critical(SERVER_ARGS_ERROR)
                raise Exception(f'\nНеверно введены параметры.\n{SERVER_ARGS_ERROR}')
    except ValueError:
        listen_port = DEFAULT_PORT
        listen_address = ''
        SERVER_LOGGER.error(f'ОШИБКА! {SERVER_ARGS_ERROR} \nБыли применены значения по умолчанию:\n'
                            f'Прослушивается порт: {listen_port}\nАдрес по умолчанию: {listen_address}')

    serv_socket = socket(AF_INET, SOCK_STREAM)
    serv_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serv_socket.bind((listen_address, listen_port))
    serv_socket.listen()

    while True:
        client_socket, client_address = serv_socket.accept()
        try:
            data_from_client = get_data(client_socket)
            SERVER_LOGGER.info(data_from_client)

            response_obj = create_response(data_from_client)
            send_data(response_obj, client_socket)

            client_socket.close()
        except (ValueError, json.JSONDecodeError):
            SERVER_LOGGER.error('Некорректное сообщение от клиента')
            client_socket.close()
        # --------- Вот это часть вызывает ошибку OSError: [Errno 9] Bad file descriptor -------------
        # Еще не разобрался до конца почему, поэтому оставил сервер в прослушивании
        # finally:
        #     serv_socket.close()


if __name__ == '__main__':
    start_server()
