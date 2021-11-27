"""Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:

Создать функцию write_order_to_json(), в которую передается 5 параметров —
товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;

Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра."""

import json


def write_order_to_json(item: str, quantity: int, price: float, buyer: str, date: str):
    dict_to_json = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }

    with open('orders.json', 'r+', encoding='utf-8') as f_n:
        objects = json.load(f_n)

        for key, value in objects.items():
            if key == "orders":
                value.append(dict_to_json)
                f_n.seek(0)
                json.dump(objects, f_n, indent=4, ensure_ascii=False)

    print('Done!')


write_order_to_json("Тостер", 5, 20.5, "Dr.Martens", "20.11.2021")
write_order_to_json("Xerox", 7, 50.78, "Mr.Fade", "12.11.2021")
write_order_to_json("Microwave", 2, 16.55, "Ms.Smith", "15.11.2021")
