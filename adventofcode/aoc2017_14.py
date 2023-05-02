from downloader import download
from aoc2017_10 import knothash
from queue import Queue

download(2017, 14)
with open('aoc2017_14input.txt') as inputfile:
    data = inputfile.read()
print(data)

grid = [''.join(f'{int(c, 16):04b}' for c in knothash(f'{data.strip()}-{n}')) for n in range(128)]
print(sum(row.count('1') for row in grid))

groups = 0
visited = set()
frontier = Queue()
for main_y, row in enumerate(grid):
    for main_x, region in enumerate(row):
        if region == '0' or (main_y, main_x) in visited:
            continue
        groups += 1
        frontier.put((main_y, main_x))
        while not frontier.empty():
            (current_y, current_x) = frontier.get()
            for neighbor_y, neighbor_x in ((current_y + 1, current_x), (current_y - 1, current_x), (current_y, current_x + 1), (current_y, current_x - 1)):
                if neighbor_y not in range(len(grid)) or neighbor_x not in range(len(grid[0])):
                    continue
                if grid[neighbor_y][neighbor_x] == '0' or (neighbor_y, neighbor_x) in visited:
                    continue
                visited.add((neighbor_y, neighbor_x))
                frontier.put((neighbor_y, neighbor_x))
print(groups)
