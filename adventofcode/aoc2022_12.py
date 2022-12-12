from downloader import download
import re
from string import ascii_lowercase as abc
from queue import PriorityQueue

download(2022, 12)
with open('aoc2022_12input.txt') as inputfile:
    data = inputfile.read()
print(data)

grid = data.splitlines()
height = len(grid)
width = len(grid[0])
#S = data.index('S')
#start = divmod(S, width + 1)
E = data.index('E')
end = divmod(E, width + 1)
grid = data.replace('S', 'a').replace('E', 'z').splitlines()

def adjacent(pos):
    y, x = pos
    return [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]

distances = set()
for a in re.finditer('a|S', data):
    start = divmod(a.start(), width + 1)
    s = a.group() == 'S'
    frontier = PriorityQueue()
    visited = {start: 0}
    frontier.put((0, start))
    while not frontier.empty():
        current_cost, current_pos = frontier.get()
        if current_pos == end:
            if s:
                print(current_cost)
            distances.add(current_cost)
            break
        current_elevation = grid[current_pos[0]][current_pos[1]]
        for next_pos in adjacent(current_pos):
            y, x = next_pos
            if not (0 <= y < height and 0 <= x < width):
                continue
            next_elevation = grid[y][x]
            if abc.index(next_elevation) > abc.index(current_elevation) + 1:
                continue
            next_cost = current_cost + 1
            if next_pos not in visited or visited[next_pos] > next_cost:
                visited[next_pos] = next_cost
                frontier.put((next_cost, next_pos))
print(min(distances))
