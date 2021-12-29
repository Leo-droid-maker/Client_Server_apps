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
from threading import Thread
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
    DESTINATION,
    EXIT,
)
from common.utils import get_data, send_data
from socket import socket, AF_INET, SOCK_STREAM
import time
from log import client_log_config
from decorators import my_log
from metaclasses import ClientVerifier

LOGGER = logging.getLogger('client')

def arg_parser():
    try:
        match argv:
            case (_, s_address, s_port_number) if (65535 > int(s_port_number) > 1024) and (
                    len(s_address.split('.')) == 4):
                server_address = s_address
                server_port = int(s_port_number)

                LOGGER.info(f'\nАдрес сервера: {server_address}\nПорт сервера: {server_port}')
            case _:
                LOGGER.critical(CLIENT_ARGS_ERROR)
                raise Exception(f'\n{CLIENT_ARGS_ERROR}')
    except ValueError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT

        LOGGER.error(f'ОШИБКА! {CLIENT_ARGS_ERROR} \nБыли применены значения по умолчанию:\n'
                     f'Адрес сервера: {server_address}\nАдрес порта: {server_port}')

    return server_address, server_port

class Client(metaclass=ClientVerifier):

    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port

    @my_log
    def create_message_to_server(self, client_socket, account_name):
        to_user = input('Введите получателя сообщения: ')
        message = input('Введите сообщение для отправки: ')

        message_dict = {
            ACTION: MESSAGE,
            USER: {
                ACCOUNT_NAME: account_name
            },
            DESTINATION: to_user,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
        try:
            send_data(message_dict, client_socket)
            LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
        except Exception:
            LOGGER.critical('Потеряно соединение с сервером.')
            exit(1)


    @my_log
    def create_presence_message_to_server(self, account_name):
        msg = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            },
        }
        if msg[ACTION] == PRESENCE and msg[USER][ACCOUNT_NAME] == account_name:
            LOGGER.info(f'Сообщение создано: {msg}')
            return msg
        LOGGER.error(f"Ошибка: Неправильно указан тип сообщения {msg}")
        raise ValueError()


    @my_log
    def create_answer(self, response_obj):
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
    def get_message_from_server(self, client_socket, account_name):
        while True:
            try:
                message = get_data(client_socket)

                match message[ACTION], message[USER][ACCOUNT_NAME], message[DESTINATION], message[MESSAGE_TEXT]:
                    case 'message', _, _, _ if message[DESTINATION] == account_name:

                        print(f'Получено сообщение от пользователя '
                              f'{message[USER][ACCOUNT_NAME]}:\n{message[MESSAGE_TEXT]}')
                        LOGGER.info(f'Получено сообщение от пользователя '
                                    f'{message[USER][ACCOUNT_NAME]}:\n{message[MESSAGE_TEXT]}')
                    case _:
                        LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
            except (OSError, ConnectionError, ConnectionAbortedError,
                    ConnectionResetError, json.JSONDecodeError):
                LOGGER.critical(f'Потеряно соединение с сервером.')
                break


    @my_log
    def create_exit_message(self, account_name):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            },
        }


    @my_log
    def user_interactive(self, client_socket, username):
        while True:
            command = input('Введите команду (message, exit): ')
            match command:
                case 'message':
                    self.create_message_to_server(client_socket, username)

                case 'exit':
                    send_data(self.create_exit_message(username), client_socket)
                    print('Завершение соединения.')
                    LOGGER.info('Завершение работы по команде пользователя.')

                    time.sleep(0.5)
                    break
                case _:
                    print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


    @my_log
    def start_client(self):
        # try:
        #     match argv:
        #         case (_, s_address, s_port_number) if (65535 > int(s_port_number) > 1024) and (
        #                 len(s_address.split('.')) == 4):
        #             server_address = s_address
        #             server_port = int(s_port_number)
        #
        #             LOGGER.info(f'\nАдрес сервера: {server_address}\nПорт сервера: {server_port}')
        #         case _:
        #             LOGGER.critical(CLIENT_ARGS_ERROR)
        #             raise Exception(f'\n{CLIENT_ARGS_ERROR}')
        # except ValueError:
        #     server_address = DEFAULT_IP_ADDRESS
        #     server_port = DEFAULT_PORT
        #
        #     LOGGER.error(f'ОШИБКА! {CLIENT_ARGS_ERROR} \nБыли применены значения по умолчанию:\n'
        #                  f'Адрес сервера: {server_address}\nАдрес порта: {server_port}')

        client_name = input('Введите имя пользователя: ')

        with socket(AF_INET, SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((self.server_address, self.server_port))

                presence_msg_to_server = self.create_presence_message_to_server(client_name)
                send_data(presence_msg_to_server, client_socket)

                response_from_server = get_data(client_socket)
                answer = self.create_answer(response_from_server)
                LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                LOGGER.error(f'Соединение с сервером {self.server_address} было потеряно.')
                exit(1)
            else:
                clnt_rcvr = Thread(target=self.get_message_from_server, args=(client_socket, client_name))
                clnt_rcvr.daemon = True
                clnt_rcvr.start()

                user_interface = Thread(target=self.user_interactive, args=(client_socket, client_name))
                user_interface.daemon = True
                user_interface.start()
                LOGGER.debug('Запущены процессы')

                while True:
                    time.sleep(1)
                    if clnt_rcvr.is_alive() and user_interface.is_alive():
                        continue
                    break

def main():
    server_address, server_port = arg_parser()
    client = Client(server_address, server_port)
    client.start_client()


if __name__ == '__main__':
    main()
