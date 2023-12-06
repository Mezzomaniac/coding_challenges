from downloader import download

download(2023, 6)
with open('aoc2023_6input.txt') as inputfile:
    data = inputfile.read()
print(data)

from functools import reduce
from math import sqrt
from operator import mul

def dist(max_time, button_time):
    return button_time * (max_time - button_time)

def ways_to_win(max_time, record):
    distances = [dist(max_time, button_time) for button_time in range(max_time + 1)]
    return len([distance for distance in distances if distance > record])

def difference_of_quadratic_formulae(max_time, record):
    record += .9
    return (max_time + sqrt(max_time ** 2 - 4 *  record)) // 2 - (max_time - sqrt(max_time ** 2 - 4 *  record)) // 2
ways_to_win = difference_of_quadratic_formulae

races = list(zip(*((int(n) for n in line.split()[1:]) for line in data.splitlines())))

print(reduce(mul, (ways_to_win(*race) for race in races), 1))

race = [int(''.join(line.split()[1:])) for line in data.splitlines()]

print(ways_to_win(*race))
