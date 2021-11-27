"""Задание на закрепление знаний по модулю yaml. Написать скрипт,
автоматизирующий сохранение данных в файле YAML-формата. Для этого:

Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €);

Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
а также установить возможность работы с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""

import yaml


def write_data_to_yaml(filename):
    first_param = ["one", "two", "three"]
    second_param = 5
    third_param = {"four": 4, "five": 5, "six": 6}

    data = {"4$": first_param, "5€": second_param, "7€": third_param}

    with open(filename, 'w', encoding='utf-8') as f_n:
        yaml.dump(data, f_n, default_flow_style=False, allow_unicode=True)

    with open(filename, 'r', encoding='utf-8') as f_n:
        print(f_n.read())


write_data_to_yaml('file.yaml')