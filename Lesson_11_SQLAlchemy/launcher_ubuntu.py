import os
import signal
from subprocess import Popen
from time import sleep

SERV_ARGS = ["gnome-terminal", "--disable-factory", "--", "bash", "-c", "python3.10 server.py -p 7777 -a 127.0.0.1"]
CLIENT_ARGS = ["gnome-terminal", "--disable-factory", "--", "bash", "-c", "python3.10 client.py 127.0.0.1 7777"]

process = []
while True:
    user_command = input("Запустить несколько клиентов (s) / Закрыть всех клиентов (x) / Выйти (q) ")

    if user_command == 'q':
        break
    elif user_command == 's':
        process.append(Popen(args=SERV_ARGS, preexec_fn=os.setpgrp))
        sleep(2)

        for i in range(2):
            process.append(Popen(args=CLIENT_ARGS, preexec_fn=os.setpgrp))

        print(' Запущено 2 клиента и сервер')

    elif user_command == "x":
        while process:
            victim = process.pop()
            os.killpg(victim.pid, signal.SIGINT)
