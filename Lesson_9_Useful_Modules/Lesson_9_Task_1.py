"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address()
"""

import platform
import socket
import subprocess
from ipaddress import ip_address as ip_adr
from socket import gethostbyname as get_ip

ip_addresses_list = [
    '0.0.0.1',
    '0.0.0.2',
    '0.0.0.3',
    '173.194.222.139',
    '5.255.255.5',
    '108.177.14.93',
    '74.6.143.25',
    'google.com',
    'yandex.ru',
    'www.yahoo.com',
    '0.0.0.4',
    '0.0.0.5',
    '0.0.0.6',
    '0.0.0.7',
    '0.0.0.8',
    '0.0.0.9',
    '0.0.1.0',
]


def get_ip_address(hosts_lst_or_single):
    if isinstance(hosts_lst_or_single, list):
        return [get_ip(host) if len(host.split('.')) == 2 or 3 else host for host in hosts_lst_or_single]
    else:
        try:
            return ip_adr(get_ip(hosts_lst_or_single))
        except socket.gaierror:
            print('Неправильно введен адресс или имя хоста.')


def host_ping(hosts_lst):
    checked_hosts_list = get_ip_address(hosts_lst)

    param = '-n1' if platform.system().lower() == 'windows' else '-c1'

    try:
        args = [["ping", param, "-w1", str(ip_adr(address))] for address in checked_hosts_list]
    except ValueError:
        print('Проверьте список хостов, присутствует неправильный адрес или имя хоста.')

    result = []
    for arg in args:
        ipv4 = str(arg[3])
        res = {}
        subproc_ping = subprocess.Popen(arg, stdout=subprocess.PIPE)

        if subproc_ping.wait() == 0:
            res["Доступный узел"] = ipv4
            print(f"{ipv4} - Узел доступен")
        else:
            res["Недоступный узел"] = ipv4
            print(f"{ipv4} - Узел недоступен")

        result.append(res)
    # print(result)
    return result


if __name__ == '__main__':
    host_ping(ip_addresses_list)
