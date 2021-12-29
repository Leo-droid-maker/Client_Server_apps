import os
import signal
from subprocess import Popen
import sys
from time import sleep

PYTHON_PATH = sys.executable
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

args_serv = ["gnome-terminal", "--disable-factory", "--", "bash", "-c", "python3.10 server.py -p 7777 -a 127.0.0.1"]
args_send = ["gnome-terminal", "--disable-factory", "--", "bash", "-c", "python3.10 client.py 127.0.0.1 7777 -m send"]
args_listen = ["gnome-terminal", "--disable-factory", "--", "bash", "-c", "python3.10 client.py 127.0.0.1 7777 -m listen"]

process = []
while True:
    user_command = input("Запустить несколько клиентов (s) / Закрыть всех клиентов (x) / Выйти (q) ")

    if user_command == 'q':
        break
    elif user_command == 's':
        process.append(Popen(args=args_serv, preexec_fn=os.setpgrp))
        sleep(2)

        for i in range(2):
            process.append(Popen(args=args_send, preexec_fn=os.setpgrp))

        for i in range(2):
            process.append(Popen(args=args_listen, preexec_fn=os.setpgrp))

        print(' Запущено 4 клиента и сервер')

    elif user_command == "x":
        while process:
            victim = process.pop()
            os.killpg(victim.pid, signal.SIGINT)
