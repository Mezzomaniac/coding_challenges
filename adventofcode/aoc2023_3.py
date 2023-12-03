from downloader import download

download(2023, 3)
with open('aoc2023_3input.txt') as inputfile:
    data = inputfile.read()

test = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''
#data = test
#print(data)

import re
from collections import defaultdict

numbers = {}
symbols = {}

for row, line in enumerate(data.splitlines()):
    numbers.update(((row, match.start(), match.end()), match.group()) for match in re.finditer('\d+', line))
    symbols.update(((row, match.start()), match.group()) for match in re.finditer('[^\d.]', line))
#print(numbers)
#print(symbols)

def adjacent(num_loc):
    row, start, end = num_loc
    return {(y, x) for y in range(row - 1, row + 2) for x in range(start - 1, end + 1)}

stars = defaultdict(list)
parts_sum = 0
for num_loc, number in numbers.items():
    if sym_locs := symbols.keys() & adjacent(num_loc):
        parts_sum += int(number)
        for sym_loc in sym_locs:
            if symbols[sym_loc] == '*':
                stars[sym_loc].append(num_loc)
print(parts_sum)

gears = {sym_loc: num_locs for sym_loc, num_locs in stars.items() if len(num_locs) == 2}
print(sum(int(numbers[num_locs[0]]) * int(numbers[num_locs[1]]) for num_locs in gears.values()))
