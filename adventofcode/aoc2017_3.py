from collections import namedtuple
from functools import lru_cache

@lru_cache()
def calc_ring_level(x):
    return (int((x - 1) ** 0.5) + 1) // 2

@lru_cache()
def calc_last_corner_square_num(x):
    return (calc_ring_level(x) * 2 - 1) ** 2

def calc_eighth_of_ring_length(x):
    return (int(calc_last_corner_square_num(x) ** 0.5) + 1) // 2

def calc_steps(x):
    ring_level = calc_ring_level(x)
    last_corner_square_num = calc_last_corner_square_num(x)
    eighth_of_ring_length = calc_eighth_of_ring_length(x)
    return ring_level + abs((x - last_corner_square_num) % (eighth_of_ring_length * 2) - eighth_of_ring_length % (eighth_of_ring_length * 2))

for x in list(range(2, 51)) + [325489]:
    ring_level = calc_ring_level(x)
    last_corner_square_num = calc_last_corner_square_num(x)
    eighth_of_ring_length = calc_eighth_of_ring_length(x)
    steps = calc_steps(x)
    print(x, ring_level, last_corner_square_num, eighth_of_ring_length, steps)

Space = namedtuple('Space', 'x y')

grid = {Space(0, 0): 1}
space = Space(0, 0)
direction = (0, 1)
x = 2
while x <= 325489:
    #print(x)
    left_direction = (direction[1], -direction[0])
    #print(left_direction)
    left_space = Space(space.x + left_direction[0], space.y + left_direction[1])
    #print(left_space)
    if not grid.get(left_space):
        direction = left_direction
    #print(direction)
    space = Space(space.x + direction[0], space.y + direction[1])
    #print(space)
    grid[space] = x
    x += 1
print(abs(space.x) + abs(space.y))

grid = {Space(0, 0): 1}
space = Space(0, 0)
direction = (0, 1)
x = 0
while x <= 325489:
    left_direction = (direction[1], -direction[0])
    left_space = Space(space.x + left_direction[0], space.y + left_direction[1])
    if not grid.get(left_space):
        direction = left_direction
    space = Space(space.x + direction[0], space.y + direction[1])
    x = sum(grid.get(Space(space.x + x, space.y + y), 0) for x in range(-1, 2) for y in range(-1, 2))
    grid[space] = x
    print(x)

