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

import logging
import time
from sys import argv
from common.config import *
from common.utils import get_data, send_data
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
from log import server_log_config
from decorators import my_log

LOGGER = logging.getLogger('server')


@my_log
def create_response_message(message, messages_list, client):
    match message[ACTION], message[TIME], message[USER][ACCOUNT_NAME]:
        case 'presence', _, 'Leo':
            LOGGER.info('Ответ сервера - 200: OK')
            send_data({RESPONSE: 200}, client)
            return
        case 'message', _, 'Leo':
            messages_list.append((message[USER][ACCOUNT_NAME], message[MESSAGE_TEXT]))
            return
        case None, None, None:
            LOGGER.error(f"Ошибка: Неправильно указан тип сообщения {message}")
            raise ValueError
        case _:
            LOGGER.error('Ответ сервера - 400: Bad request')
            send_data({RESPONSE: 400, ERROR: "Bad request"}, client)
            return


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
                LOGGER.info(f'\nПрослушивается: {listen_address}\nПорт: {listen_port}')
            case _:
                LOGGER.critical(SERVER_ARGS_ERROR)
                raise Exception(f'\nНеверно введены параметры.\n{SERVER_ARGS_ERROR}')
    except ValueError:
        listen_port = DEFAULT_PORT
        listen_address = ''
        LOGGER.error(f'ОШИБКА! {SERVER_ARGS_ERROR} \nБыли применены значения по умолчанию:\n'
                     f'Прослушивается порт: {listen_port}\nАдрес по умолчанию: {listen_address}')

    serv_socket = socket(AF_INET, SOCK_STREAM)
    serv_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serv_socket.bind((listen_address, listen_port))
    serv_socket.settimeout(0.5)

    clients = []
    messages = []

    serv_socket.listen(MAX_CONNECTIONS)

    while True:
        try:
            client_socket, client_address = serv_socket.accept()
        except OSError:
            pass
        else:
            LOGGER.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client_socket)

        recv_data_lst = []
        send_data_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    create_response_message(get_data(client_with_message), messages, client_with_message)
                except:
                    LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_data(message, waiting_client)
                except:
                    LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    start_server()
