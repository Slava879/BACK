n = int(input('Введите количество чисел:\n>>>'))
numbers = [int(input('>>>')) for number in range(n)]

output_numbers = []

for number1 in range(len(numbers)):
    _min, number = 10 ** 10, 0
    for number2 in range(len(numbers)):
        if number1 != number2:
            delta = abs(numbers[number1] - numbers[number2])
            if delta < _min:
                _min, number = delta, numbers[number2]
            elif delta == _min:
                _min, number = delta, min(numbers[number2], number)
    output_numbers.append(number)

print(' '.join(map(str, output_numbers)))


