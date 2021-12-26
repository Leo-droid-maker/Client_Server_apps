"""
Реализовать метакласс ClientVerifier,
выполняющий базовую проверку класса «Клиент» (для некоторых проверок уместно использовать модуль dis):
отсутствие вызовов accept и listen для сокетов;
использование сокетов для работы по TCP;

Реализовать метакласс ServerVerifier, выполняющий базовую проверку класса «Сервер»:
отсутствие вызовов connect для сокетов;
использование сокетов для работы по TCP.
"""

import dis
import inspect
import logging

CLIENT_LOGGER = logging.getLogger('client')
SERVER_LOGGER = logging.getLogger('server')


class ClientVerifier(type):
    def __init__(cls, name, bases, clsdict):

        methods = []

        for key, value in clsdict.items():
            if inspect.isfunction(value):
                ret = dis.get_instructions(value)
                for i in ret:
                    match i.opname:
                        case ('LOAD_GLOBAL' | 'LOAD_METHOD') if i.argval not in methods:
                            methods.append(i.argval)
                            # CLIENT_LOGGER.info(i.argval)

        if 'accept' in methods or 'listen' in methods or 'socket' in methods:
            CLIENT_LOGGER.critical('Клиентское приложение не должно использовать вызов accept или listen!')

        # print(methods)
        super().__init__(name, bases, clsdict)


class ServerVerifier(type):
    def __init__(cls, name, bases, clsdict):

        methods = []
        attrs = []

        for key, value in clsdict.items():
            if inspect.isfunction(value):
                ret = dis.get_instructions(value)
                for i in ret:
                    # print(i.opname)
                    match i.opname:
                        case ('LOAD_GLOBAL' | 'LOAD_METHOD') if i.argval not in methods:
                            methods.append(i.argval)
                        case 'LOAD_ATTR' if i.argval not in attrs:
                            attrs.append(i.argval)

        # print(methods)

        if 'connect' in methods:
            SERVER_LOGGER.critical('Использование метода connect недопустимо в серверном классе')

        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            SERVER_LOGGER.critical('Некорректная инициализация сокета.')

        super().__init__(name, bases, clsdict)
