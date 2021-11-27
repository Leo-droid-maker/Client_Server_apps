"""1. Каждое из слов «разработка», «сокет», «декоратор» представить в 
строковом формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые представление в 
формат Unicode и также проверить тип и содержимое переменных."""

DEVELOPING = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
SOCKET = '\u0441\u043e\u043a\u0435\u0442'
DECORATOR = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'


def check_type_and_unicode(words):
    match words:
        case (str(first), str(second), str(third)) if first == DEVELOPING and second == SOCKET and third == DECORATOR:
            return f'"{first}", "{second}", "{third}" is exacly equals to:\n \
                DEVELOPING = {str.encode(DEVELOPING, encoding="utf-8")} - {first},\n \
                SOCKET = {str.encode(SOCKET, encoding="utf-8")} - {second},\n \
                DECORATOR = {str.encode(DECORATOR, encoding="utf-8")} - {third}'
        case _:
            raise ValueError("One or more given words is unsuitable. Or given 4 or more params")


print(check_type_and_unicode(('разработка', 'сокет', 'декоратор')))
