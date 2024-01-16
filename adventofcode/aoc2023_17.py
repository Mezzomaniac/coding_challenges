from downloader import download

download(2023, 17)
with open('aoc2023_17input.txt') as inputfile:
    data = inputfile.read()
test_data = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''
#data = test_data
print(data)

from collections import deque, namedtuple
from dataclasses import dataclass, field
from functools import lru_cache
from queue import PriorityQueue

grid = [[int(block) for block in line] for line in data.splitlines()]
height = len(grid)
width = len(grid[0])

MAX_REPEATED_STEPS = 3
MIN_REPEATED_STEPS = 0
MAX_REPEATED_STEPS = 10
MIN_REPEATED_STEPS = 4

Coord = namedtuple('Coord', 'y x')

@dataclass(frozen=True)
class CrucibleState:
    pos: Coord
    last_step: Coord|None
    num_repeated_steps: int=0

@dataclass(order=True)
class PrioritisedState:
    priority: int
    state: CrucibleState=field(compare=False)


DIRS = [Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)]

@lru_cache()
def movement_options(last_step: Coord|None, num_repeated_steps: int):
    if last_step and num_repeated_steps < MIN_REPEATED_STEPS:
        return [last_step]
    options = []
    for dir in DIRS:
        if last_step and (dir == Coord(-last_step.y, -last_step.x) or dir == last_step and num_repeated_steps == MAX_REPEATED_STEPS):
            continue
        options.append(dir)
    return options

frontier = PriorityQueue()
start = CrucibleState(Coord(0, 0), None)
distance = height + width - 2
nearest = distance
frontier.put(PrioritisedState(0, start))
heat_losses = {start: 0}
while not frontier.empty():
    current_state = frontier.get().state
    distance = height + width - 2 - current_state.pos.y - current_state.pos.x
    if distance < nearest:
        nearest = distance
        print(f'{distance=}')
    if current_state.pos == Coord(height - 1, width - 1):
        if current_state.num_repeated_steps < MIN_REPEATED_STEPS:
            continue
        print(heat_losses[current_state])
        break
    for next_step in movement_options(current_state.last_step, current_state.num_repeated_steps):
        next_pos = Coord(current_state.pos.y + next_step.y, current_state.pos.x + next_step.x)
        if not (0 <= next_pos.y < height and 0 <= next_pos.x < width):
            continue
        next_heat_loss = heat_losses[current_state] + grid[next_pos.y][next_pos.x]
        if next_step == current_state.last_step:
            next_num_repeated_steps = current_state.num_repeated_steps + 1
        else:
            next_num_repeated_steps = 1
        next_state = CrucibleState(next_pos, next_step, next_num_repeated_steps)
        if next_state in heat_losses and heat_losses[next_state] <= next_heat_loss:
            continue
        priority = heat_losses[current_state]
        frontier.put(PrioritisedState(priority, next_state))
        heat_losses[next_state] = next_heat_loss

