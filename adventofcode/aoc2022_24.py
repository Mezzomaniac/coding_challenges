from downloader import download
from queue import PriorityQueue
from functools import lru_cache

download(2022, 24)
with open('aoc2022_24input.txt') as inputfile:
    data = inputfile.read()
test = '''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''
#data = test
print(data)

@lru_cache()
def point_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

@lru_cache()
def move_options(pos):
    options = {pos, point_add(pos, (-1, 0)), point_add(pos, (1, 0)), point_add(pos, (0, -1)), point_add(pos, (0, 1))}
    options = {option for option in options if 0 <= option[0] <= width and 0 <= option[1] <= height}
    return options

class HorizontalBlizzard:
    
    def __init__(self, pos, direction):
        self.x, self.y = pos
        dir = 1 if direction == '>' else -1
        self.dir = dir
        
    def location(self, round):
        return (((self.x + self.dir * round - 1) % (width - 1)) + 1, self.y)

class VerticalBlizzard:
    
    def __init__(self, pos, direction):
        self.x, self.y = pos
        dir = 1 if direction == 'v' else -1
        self.dir = dir
    
    def location(self, round):
        return (self.x, ((self.y + self.dir * round - 1) % (height - 1)) + 1)

def create_blizzard(pos, direction):
    if direction in '<>':
        return HorizontalBlizzard(pos, direction)
    elif direction in '^v':
        return VerticalBlizzard(pos, direction)

blizzards = set()
walls = set()
for y, row in enumerate(data.splitlines()):
    for x, space in enumerate(row):
        if space == '#':
            walls.add((x, y))
        elif space != '.':
            blizzards.add(create_blizzard((x, y), space))
        elif space == '.':
            goal = (x, y)
start = (data.index('.'), 0)
width = x
height = y

def heuristic(pos, goal):
    return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])

priority = heuristic(start, goal)
visited = {(0, start)}
frontier = PriorityQueue()
frontier.put((priority, (0, start)))
leg = 1
while not frontier.empty():
    priority, (current_cost, current) = frontier.get()
    #print(current_cost, current)
    if current == goal:
        print(current_cost)
        if leg < 3:
            start, goal = goal, start
            priority = heuristic(start, goal)
            visited = {(current_cost, start)}
            frontier = PriorityQueue()
            frontier.put((priority, (current_cost, start)))
            leg += 1
        else:
            break
    next_cost = current_cost + 1
    next_blizzards = {blizzard.location(next_cost) for blizzard in blizzards}
    for next in move_options(current):
        if next in walls or next in next_blizzards:
            continue
        if (next_cost, next) not in visited:
            visited.add((next_cost, next))
            priority = heuristic(next, goal) + next_cost
            frontier.put((priority, (next_cost, next)))
