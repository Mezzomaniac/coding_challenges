DEPTH = 10914
TARGET = (9, 739, 'T')

from functools import lru_cache
from queue import PriorityQueue

@lru_cache(maxsize=None)
def geologic_index(coord):
    #print('GI', coord)
    x, y = coord
    if coord in ((0, 0), TARGET[:2]):
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return erosion_level((x-1, y)) * erosion_level((x, y-1))

@lru_cache(maxsize=None)
def erosion_level(coord):
    #print('EL', coord)
    return (geologic_index(coord) + DEPTH) % 20183

@lru_cache(maxsize=None)
def region_type(coord):
    #print('RT', coord)
    return erosion_level(coord) % 3

#[region_type((x, y)) for x in range(30) for y in range(760)]

risk_level = sum(region_type((x, y)) for x in range(10) for y in range(740))
print(risk_level)


REGION_TOOLS = ('TC', 'CN', 'TN')

def neighbors(coord):
    #print('Ne', coord)
    x, y, tool = coord
    other_tool = REGION_TOOLS[region_type((x, y))].replace(tool, '')
    result = [(a, b, tool) for a, b in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)) if a >= 0 and b >= 0 and tool in REGION_TOOLS[region_type((a, b))]]
    result.append((x, y, other_tool))
    return result

def heuristic(coord):
    return abs(TARGET[0] - coord[0]) + abs(TARGET[1] - coord[1])

#print('\n' * 10)
frontier = PriorityQueue()
start = (0, 0, 'T')
came_from = {start: None}
cost_so_far = {start: 0}
frontier.put((0, start))
while not frontier.empty():
    current = frontier.get()[1]
    #print(current, region_type(current[:2]))
    if current == TARGET:
        print(cost_so_far[current])
        break
    for next in neighbors(current):
        #print(next, region_type(next[:2]))
        new_cost = 1 if next[2] == current[2] else 7
        #print(new_cost)
        cost = cost_so_far[current] + new_cost
        #print(cost)
        if next not in cost_so_far or cost < cost_so_far[next]:
            cost_so_far[next] = cost
            priority = cost + heuristic(next[:2])
            #print(priority)
            frontier.put((priority, next))
            came_from[next] = current
    #print()
