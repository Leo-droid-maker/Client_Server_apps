"""
клиент отправляет запрос серверу;
сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде отдельных скриптов,
содержащих соответствующие функции.
Функции сервера: принимает сообщение клиента; формирует ответ клиенту; отправляет ответ клиенту;
имеет параметры командной строки: -p <port> — TCP-порт для работы (по умолчанию использует 7777); -a <addr> —
IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""


import json
from sys import argv
from common.config import *
from common.utils import get_data, send_data
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def create_response(message):
    match message[ACTION], message[TIME], message[USER][ACCOUNT_NAME]:
        case 'presence', _, 'Leo':
            return {RESPONSE: 200}
        case None, None, None:
            raise ValueError
        case _:
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
            case _:
                raise Exception(f'\nНеверно введены параметры.\n{SERVER_ARGS_ERROR}')
    except ValueError:
        listen_port = DEFAULT_PORT
        listen_address = ''
        print(f'ОШИБКА! {SERVER_ARGS_ERROR} \nБыли применены значения по умолчанию:\n'
              f'Прослушивается порт: {listen_port}\nАдрес по умолчанию: {listen_address}')

    serv_socket = socket(AF_INET, SOCK_STREAM)
    serv_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serv_socket.bind((listen_address, listen_port))
    serv_socket.listen()

    while True:
        client_socket, client_address = serv_socket.accept()
        try:
            data_from_client = get_data(client_socket)
            print(data_from_client)

            response_obj = create_response(data_from_client)
            send_data(response_obj, client_socket)

            client_socket.close()
        except (ValueError, json.JSONDecodeError):
            print('Некорректное сообщение от клиента')
            client_socket.close()
        # --------- Вот это часть вызывает ошибку OSError: [Errno 9] Bad file descriptor -------------
        # Еще не разобрался до конца почему, поэтому оставил сервер в прослушивании
        # finally:
        #     serv_socket.close()


if __name__ == '__main__':
    start_server()
