"""4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» 
из строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode)."""


def encoding_and_decoding(words):
    encoded_strings = [word.encode('utf-8') for word in words]
    decoded_bytes = [byte.decode('utf-8') for byte in encoded_strings]

    return encoded_strings, decoded_bytes


result_of_bytes, result_of_strings = encoding_and_decoding(("разработка", "администрирование", "protocol", "standard"))

print(f' List of encoded strings: {result_of_bytes},\n{"-" * 50}\nList of decoded bytes: {result_of_strings}')
