from copy import deepcopy
from functools import lru_cache
import itertools
from queue import PriorityQueue
from time import time

class Floors:
    
    def __init__(self, floors, elevator):
        self.floors = floors
        self.elevator = elevator
    
    def __eq__(self, other):
        return hash(self) == hash(other)
        
    def __lt__(self, other):
        return hash(self) < hash(other)
    
    def __hash__(self):
        return hash((tuple(frozenset(floor) for floor in self.floors), self.elevator))
    
    def __repr__(self):
        return f'Floors({self.floors}, {self.elevator})'
    
    def __str__(self):
        return '\n'.join(str(floor)  for floor in reversed(self.floors)) + f'\nE={self.elevator}'

@lru_cache(maxsize=None)
def cargo_options(items):
    return list(itertools.chain(itertools.combinations(items, 2), itertools.combinations(items, 1)))

def categorise_items(items):
    generators = {item[0] for item in items if item.endswith('G')}
    microchips = {item[0] for item in items if item.endswith('M')}
    return generators, microchips

@lru_cache(maxsize=None)
def irradiated(items):
    generators, microchips = categorise_items(items)
    return generators and microchips - generators

@lru_cache(maxsize=None)
def score(floors):
    return 10 * len(floors.floors[-1]) + 9 * len(floors.floors[-2]) + 8 * len(floors.floors[-3])

t = time()
start = Floors([{'TG', 'TM', 'LG', 'SG'}, {'LM', 'SM'}, {'PG', 'PM', 'RG', 'RM'}, set()], 0)
start.floors[0] |= {'EG', 'EM', 'DG', 'DM'}
#start = Floors([{'HM', 'LM'}, {'HG'}, {'LG'}, set()], 0)
#came_from = {start: None}
costs = {start: 0}
frontier = PriorityQueue()
frontier.put((0, start))
maxcost = 0
while not frontier.empty():
    current = frontier.get()[1]
    #print(current, costs[current])
    if costs[current] > maxcost:
        maxcost = costs[current]
        print(maxcost)
    if not set.union(*current.floors[:-1]):
        print(costs[current])
        break
    for step in {(current.elevator + change) for change in (-1, 1)}:
        if step not in range(4):
            continue
        for cargo in cargo_options(frozenset(current.floors[current.elevator])):
            cargo = frozenset(cargo)
            if irradiated(cargo | current.floors[step]) or irradiated(frozenset(current.floors[current.elevator]) - cargo):
                continue
            next = Floors(deepcopy(current.floors), step)
            next.floors[current.elevator] -= cargo
            next.floors[step] |= cargo
            cost = costs[current] + 1
            if cost < costs.get(next, cost + 1):
                costs[next] = cost
                #came_from[next] = current
                priority = cost - score(next)
                frontier.put((priority, next))
print(time() - t)
