from downloader import download

download(2023, 1)
with open('aoc2023_1input.txt') as inputfile:
    data = inputfile.read()
print(data)

import re
from string import ascii_lowercase as abc

total = 0
for line in data.splitlines():
    stripped = line.strip(abc)
    total += int(stripped[0] + stripped[-1])
print(total)

numbers = dict(zip(['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'], (str(n) for n in range(10))))

pattern = '|'.join(numbers.keys()) + '|\d'
reverse_pattern = '|'.join(number[::-1] for number in numbers.keys()) + '|\d'
total = 0
for line in data.splitlines():
    match1 = re.search(pattern, line).group()
    match2 = re.search(reverse_pattern, line[::-1]).group()[::-1]
    digits = ''
    for digit in (match1, match2):
        digits += numbers.get(digit, digit)
    total += int(digits)
print(total)
