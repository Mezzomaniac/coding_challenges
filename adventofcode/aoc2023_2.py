from downloader import download

download(2023, 2)
with open('aoc2023_2input.txt') as inputfile:
    data = inputfile.read()
print(data)

import re

result1 = 0
result2 = 0
for line in data.splitlines():
    game = int(re.search('\d+', line).group())
    reds, greens, blues = ([int(n) for n in re.findall(f'(\d+) {color}', line)] for color in ('red', 'green', 'blue'))
    if all(red <= 12 for red in reds) and  all(green <= 13 for green in greens) and  all(blue <= 14 for blue in blues) :
        result1 += game
    result2 += max(reds) * max(greens) * max(blues)
print(result1)
print(result2)
