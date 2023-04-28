from downloader import download
from collections import defaultdict
import operator

download(2017, 8)
with open('aoc2017_8input.txt') as inputfile:
    data = inputfile.read()
print(data)

operations = {'inc': operator.add, 'dec': operator.sub}

registers = defaultdict(int)
highest = 0
for line in data.splitlines():
    parts = line.split()
    register = parts[0]
    op = operations[parts[1]]
    if eval(f'{registers[parts[4]]} {parts[5]} {parts[6]}'):
        registers[register] = op(registers[register], int(parts[2]))
    highest = max(highest, registers[register])
print(max(registers.values()))
print(highest)
