"""
1. Продолжая задачу логирования, реализовать декоратор @log, фиксирующий обращение к декорируемой функции.
Он сохраняет ее имя и аргументы.

2. В декораторе @log реализовать фиксацию функции, из которой была вызвана декорированная.
...в логе должна быть отражена информация:
"<дата-время> Функция func_z() вызвана из функции main"

"""

import logging
from sys import argv
import traceback

match argv[0]:
    case 'client.py':
        LOGGER = logging.getLogger('client')
    case 'server.py':
        LOGGER = logging.getLogger('server')


def my_log(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        parent_func = str(traceback.extract_stack()[1]).split(' ')[-1].replace('>', '')

        LOGGER.debug(f'Вызвана функция {func.__name__} c аргументами {args}, {kwargs}')
        LOGGER.info(f'Вызвана из функции-предка: {parent_func}')
        return result

    return wrapper
