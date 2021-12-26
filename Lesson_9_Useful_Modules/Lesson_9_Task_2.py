"""
Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""

from Lesson_9_Task_1 import get_ip_address, host_ping


def host_range_ping():
    first_ip = input("Введите первый адрес или имя хоста: ")
    ipv4_first = get_ip_address(first_ip)
    last_oct = int(str(ipv4_first).split('.')[3])

    while True:
        end_ip = input("Сколько адресов проверить?: ")
        if not end_ip.isnumeric():
            print("Необходимо ввести число")
        else:
            if (last_oct + int(end_ip)) > 255 + 1:
                print(f"Можем менять только последний октет, т.е. максимальное число хостов {255 + 1 - last_oct}")
            else:
                break

    result_list = [(str(ipv4_first + i)) for i in range(int(end_ip))]

    return host_ping(result_list)


if __name__ == "__main__":
    host_range_ping()
