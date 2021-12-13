"""3. Определить, какие из слов «attribute», «класс», «функция», «type» 
невозможно записать в байтовом типе."""


def check_for_bytes(words):
    for word in words:
        try:
            eval(f"b'{word}'")
        except SyntaxError:
            print(f'Cant to convert word: "{word}" to bytes')


check_for_bytes(('attribute', 'класс', 'функция', 'type'))
