"""2. Каждое из слов «class», «function», «method» записать в байтовом типе
 без преобразования в последовательность кодов (не используя методы encode и decode)
  и определить тип, содержимое и длину соответствующих переменных."""


def to_bytes(words):
    try:
        list_of_words = [[ord(char) for char in word] for word in words]
        list_of_bytes = [bytes(byte_word) for byte_word in list_of_words]
        for el in list_of_bytes:
            print(f'class - {type(el)},\nlength - {len(el)},\n{el}\n')
    except ValueError:
        print("Words must be in ASCII")


to_bytes(("class", "function", "method"))
