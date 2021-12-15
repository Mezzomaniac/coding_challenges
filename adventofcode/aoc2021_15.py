from downloader import download
from queue import PriorityQueue

download(2021, 15)
with open('aoc2021_15input.txt') as inputfile:
    grid = inputfile.read().splitlines()

len_x = len(grid[0])
len_y = len(grid)
GOAL = (len_y - 1, len_x - 1)
GOAL = (len_y * 5 - 1, len_x * 5 - 1)

def adjacents(coord):
    y, x = coord
    results = set()
    for dx in (-1, 1):
        new_x = x + dx
        #if new_x not in (-1, len_x):
        if new_x not in (-1, len_x * 5):
            results.add((y, new_x))
    for dy in (-1, 1):
        new_y = y + dy
        #if new_y not in (-1, len_y):
        if new_y not in (-1, len_y * 5):
            results.add((new_y, x))
    return results

def find_risk(coord):
    y, x = coord
    y_repeats, base_y = divmod(y, len_y)
    x_repeats, base_x = divmod(x, len_x)
    risk = int(grid[base_y][base_x]) + y_repeats + x_repeats
    if risk > 9:
        risk -= 9
    return risk

frontier = PriorityQueue()
start = (0, (0, 0))
visited = {(0, 0): 0}
frontier.put(start)
while not frontier.empty():
    total_risk, current_space = frontier.get()
    if current_space == GOAL:
        print(total_risk)
        break
    for adjacent in adjacents(current_space):
        if adjacent in visited:
            continue
        y, x = adjacent
        #risk = int(grid[y][x]) + total_risk
        risk = find_risk(adjacent) + total_risk
        frontier.put((risk, adjacent))
        if adjacent not in visited or visited[adjacent] < risk:
            visited[adjacent] = risk
