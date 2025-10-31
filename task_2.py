import re
from decimal import Decimal
import argparse


def chets_func(file_path):

    users = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:

            string = re.match(r'"([^"]+)"\s*-\s*(\d+):\s*([+-])([\d\.]+)', line)
            if not string:
                print(f'Ошибка в строке: {line}')
                continue
            name, chet_number, symbol, summa = string.groups()
            summa = Decimal(f'{symbol}{summa}')

            if name not in users:
                users[name] = {}
            if chet_number not in users[name]:
                users[name][chet_number] = Decimal('0')
            users[name][chet_number] += summa

    for name, chets in users.items():
        line_print, flag = f'{name}', True
        for chet_number, summa in chets.items():
            if flag:
                line_print += f' - {chet_number}: {summa}'
                flag = False
            else:
                line_print += f', {chet_number}: {summa}'
        print(line_print)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str)
    args = parser.parse_args()
    file_path = args.file_path
    chets_func(file_path)