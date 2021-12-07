from downloader import download

download(2021, 7)
with open('aoc2021_7input.txt') as inputfile:
    input = [int(n) for n in inputfile.read().split(',')]
print(input)

def triangular(n):
    return (n ** 2 + n) // 2

least_fuel = float('inf')
best_space = None
for space in range(min(input), max(input) + 1):
    #fuel = sum(abs(pos - space) for pos in input)
    fuel = sum(triangular(abs(pos - space)) for pos in input)
    if fuel < least_fuel:
        least_fuel = fuel
        best_space = space
print(least_fuel)


from aoc2019intcode import Intcode
easter_egg = Intcode(input)
print(easter_egg.to_ascii(easter_egg.run()))
