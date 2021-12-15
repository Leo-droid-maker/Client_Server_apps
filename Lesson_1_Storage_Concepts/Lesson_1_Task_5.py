"""5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
 преобразовать результаты из байтовового в строковый тип на кириллице."""

import subprocess
import chardet
import platform


def check_ping(links):
    param = '-n4' if platform.system().lower() == 'windows' else '-c4'
    args = [["ping", param, "-w100", link] for link in links]
    for arg in args:
        subproc_ping = subprocess.Popen(arg, stdout=subprocess.PIPE)
        for line in subproc_ping.stdout:
            result = chardet.detect(line)
            line = line.decode(result['encoding']).encode('utf-8')
            print(line.decode('utf-8'))


check_ping(('yandex.ru', 'google.com'))
