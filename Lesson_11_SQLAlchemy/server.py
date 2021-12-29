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
from sys import argv
from common.config import *
from common.utils import get_data, send_data
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
from log import server_log_config
from decorators import my_log
from descriptors import PortVerify
from metaclasses import ServerVerifier
from server_db_handler import ServerDatabase

LOGGER = logging.getLogger('server')


def arg_parser():
    # try:
    #     match argv:
    #         case (_, p, port_number, a, address) \
    #             if p == '-p' \
    #                and a == '-a' \
    #                and (65535 > int(port_number) > 1024) \
    #                and (len(address.split('.')) == 4):
    #             listen_port = int(port_number)
    #             listen_address = address
    #             LOGGER.info(f'\nПрослушивается: {listen_address}\nПорт: {listen_port}')
    #         case _:
    #             LOGGER.critical(SERVER_ARGS_ERROR)
    #             raise Exception(f'\nНеверно введены параметры.\n{SERVER_ARGS_ERROR}')
    # except ValueError:
    #     listen_port = DEFAULT_PORT
    #     listen_address = ''
    #     LOGGER.error(f'ОШИБКА! {SERVER_ARGS_ERROR} \nБыли применены значения по умолчанию:\n'
    #                  f'Прослушивается порт: {listen_port}\nАдрес по умолчанию: {listen_address}')

    match argv:
        case (_, p, port_number, a, address) \
            if p == '-p' \
               and a == '-a' \
               and (len(address.split('.')) == 4):
            listen_port = int(port_number)
            listen_address = address
            LOGGER.info(f'\nПрослушивается: {listen_address}\nПорт: {listen_port}')

    return listen_address, listen_port


class Server(metaclass=ServerVerifier):
    port = PortVerify()

    def __init__(self, listen_address, listen_port, database):
        self.listen_address = listen_address
        self.port = listen_port
        self.database = database

    @my_log
    def create_response_message(self, message, messages_list, client, clients, names):
        match message[ACTION], message[TIME], message[USER][ACCOUNT_NAME]:
            case 'presence', _, _ if message[USER][ACCOUNT_NAME] not in names.keys():
                names[message[USER][ACCOUNT_NAME]] = client
                client_ip, client_port = client.getpeername()

                self.database.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port)

                for user in sorted(self.database.active_users_list()):
                    print(
                        f'Пользователь {user[0]}, подключен: {user[1]}:{user[2]}, время установки соединения: {user[3]}')

                # print(sorted(self.database.active_users_list()))

                send_data({RESPONSE: 200}, client)
                return
            case 'presence', _, _ if message[USER][ACCOUNT_NAME] in names.keys():
                send_data({RESPONSE: 400, ERROR: 'Имя пользователя уже занято.'}, client)
                clients.remove(client)
                client.close()
                return
            case 'message', _, _ if DESTINATION in message and MESSAGE_TEXT in message:
                messages_list.append(message)

                return
            case 'exit', _, _:
                self.database.user_logout(message[USER][ACCOUNT_NAME])

                for user in sorted(self.database.login_history(message[USER][ACCOUNT_NAME])):
                    print(f'Пользователь: {user[0]} время входа: {user[1]}. Вход с: {user[2]}:{user[3]}')

                clients.remove(names[message[USER][ACCOUNT_NAME]])
                names[message[USER][ACCOUNT_NAME]].close()
                del names[message[USER][ACCOUNT_NAME]]
                return
            case None, None, None:
                LOGGER.error(f"Ошибка: Неправильно указан тип сообщения {message}")
                raise ValueError
            case _:
                LOGGER.error('Ответ сервера - 400: Bad request')
                send_data({RESPONSE: 400, ERROR: "Bad request"}, client)
                return

    @my_log
    def message_handler(self, message, names, listen_sockets):
        if message[DESTINATION] in names and names[message[DESTINATION]] in listen_sockets:
            send_data(message, names[message[DESTINATION]])
            LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                        f'от пользователя {message[USER][ACCOUNT_NAME]}.')
        elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_sockets:
            raise ConnectionError
        else:
            LOGGER.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
                f'отправка сообщения невозможна.')

    def start_server(self):

        with socket(AF_INET, SOCK_STREAM) as serv_socket:
            serv_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            serv_socket.bind((self.listen_address, self.port))
            serv_socket.settimeout(0.5)

            clients = []
            messages = []

            names = {}

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
                            self.create_response_message(get_data(client_with_message), messages, client_with_message,
                                                         clients,
                                                         names)
                        except:
                            LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                            clients.remove(client_with_message)

                for i in messages:
                    try:
                        self.message_handler(i, names, send_data_lst)
                    except Exception:
                        LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                        clients.remove(names[i[DESTINATION]])
                        del names[i[DESTINATION]]

                messages.clear()


def main():
    listen_address, listen_port = arg_parser()
    database = ServerDatabase()
    server = Server(listen_address, listen_port, database)
    server.daemon = True
    server.start_server()


if __name__ == '__main__':
    main()
