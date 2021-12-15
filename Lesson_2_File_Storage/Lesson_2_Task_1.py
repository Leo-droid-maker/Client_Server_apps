"""Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:

-Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы»,  «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно получиться четыре списка —
например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции создать главный список для
хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета в виде списка:
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

-Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

-Проверить работу программы через вызов функции write_to_csv().
"""

import csv
import re
from chardet import UniversalDetector

DETECTOR = UniversalDetector()
FILES = ['info_1.txt', 'info_2.txt', 'info_3.txt']


def get_data(files):
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    for file in files:
        with open(file, 'rb') as f_n:
            for i in f_n:
                DETECTOR.feed(i)
                if DETECTOR.done:
                    break
            DETECTOR.close()

        with open(file, 'r', encoding=DETECTOR.result['encoding']) as f:
            content = f.read()

            os_prod_list = re.findall('Изготовитель системы:\s+(\w+)', content)
            os_name_list = re.findall('Название ОС:\s+([\w\.\s\w]+)\n', content)
            os_code_list = re.findall('Код продукта:\s+([\w\-]+\w+)', content)
            os_type_list = re.findall('Тип системы:\s+([\w\-\w\s\w].+)', content)

            main_data.extend([[*os_prod_list, *os_name_list, *os_code_list, *os_type_list]])

    return main_data


def write_to_csv(csv_file):
    data = get_data(FILES)
    with open(csv_file, 'w', encoding='utf-8') as f_n:
        f_n_writer = csv.writer(f_n)
        for row in data:
            f_n_writer.writerow(row)

    with open(csv_file, 'r', encoding='utf-8') as f_n:
        return f_n.read()


print(write_to_csv('file_with_csv.csv'))
