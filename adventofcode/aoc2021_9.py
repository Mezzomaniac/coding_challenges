from downloader import download
from queue import Queue

download(2021, 9)
with open('aoc2021_9input.txt') as inputfile:
    heightmap = [[int(n) for n in line] for line in inputfile.read().splitlines()]
print(heightmap)

def adjacent_coords(y, x):
    coords = {(y, x+1), (y, x-1), (y+1, x), (y-1, x)}
    if x-1 < 0:
        coords.remove((y, x-1))
    if y-1 < 0:
        coords.remove((y-1, x))
    return coords

total_risk_level = 0
basins = {}
for y, line in enumerate(heightmap):
    for x, height in enumerate(line):
        low_point = True
        for adjacent_y, adjacent_x in adjacent_coords(y, x):
            try:
                adjacent_height = heightmap[adjacent_y][adjacent_x]
            except IndexError:
                continue
            if adjacent_height <= height:
                low_point = False
                break
        if low_point:
            total_risk_level += 1 + height
            basins[(y, x)] = set()
print(total_risk_level)

for start in basins:
    frontier = Queue()
    frontier.put(start)
    while not frontier.empty():
        point = frontier.get()
        y, x = point
        try:
            height = heightmap[y][x]
        except IndexError:
            continue
        if height != 9 and point not in basins[start]:
            basins[start].add(point)
            for adjacent_coord in adjacent_coords(*point):
                frontier.put(adjacent_coord)

basin_sizes = (len(basin) for basin in basins.values())
answer = 1
for basin in sorted(basin_sizes, reverse=True)[:3]:
    answer *= basin
print(answer)
