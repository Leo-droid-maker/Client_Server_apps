"""6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое."""


def check_file(filename):
    f_n = open(f'{filename}', "w")
    f_n.write("сетевое программирование\nсокет\nдекоратор")
    f_n.close()
    print(f'The encoding of this file is: {f_n.encoding}')

    with open(f'{filename}', 'r', encoding='utf-8') as f:
        content = f.readlines()
        for line in content:
            print(line)


check_file('test_file.txt')
