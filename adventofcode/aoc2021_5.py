from downloader import download
from collections import defaultdict

download(2021, 5)
with open('aoc2021_5input.txt') as inputfile:
    input = [[[int(n) for n in pos.split(',')] for pos in line.split(' -> ')] for line in inputfile.readlines()]
print(input)


grid = defaultdict(int)
for (x1, y1), (x2, y2) in input:
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            grid[(x1, y)] += 1
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            grid[(x, y1)] += 1
print(len(set(point for point in grid if grid[point] > 1)))


def get_range(start, end):
    if end > start:
        return range(start, end + 1)
    return range(start, end - 1, -1)

grid = defaultdict(int)
for (x1, y1), (x2, y2) in input:
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            grid[(x1, y)] += 1
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            grid[(x, y1)] += 1
    else:
        for point in zip(get_range(x1, x2), get_range(y1, y2)):
            grid[point] += 1
print(len(set(point for point in grid if grid[point] > 1)))
