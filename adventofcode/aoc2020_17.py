initial = '''.#..####
.#.#...#
#..#.#.#
###..##.
..##...#
..##.###
#.....#.
..##..##'''

from functools import lru_cache

@lru_cache(maxsize=None)
def neighbors_coords(cube):
    result = {(x, y, z) for x in range(cube[0]-1, cube[0]+2) for y in range(cube[1]-1, cube[1]+2) for z in range(cube[2]-1, cube[2]+2)}
    result.remove(cube)
    return result

@lru_cache(maxsize=None)
def neighbors_coords_4d(cube):
    result = {(x, y, z, w) for x in range(cube[0]-1, cube[0]+2) for y in range(cube[1]-1, cube[1]+2) for z in range(cube[2]-1, cube[2]+2) for w in range(cube[3]-1, cube[3]+2)}
    result.remove(cube)
    return result

neighbors_coords = neighbors_coords_4d

@lru_cache(maxsize=None)
def next_state(state, active_neighbors):
    if state == '#' and active_neighbors not in range(2, 4):
        return '.'
    if state == '.' and active_neighbors == 3:
        return '#'
    return state

def cycle(cubes):
    new = {}
    for cube, state in cubes.items():
        neighbors = neighbors_coords(cube)
        active_neighbors = sum(cubes.get(neighbor, '.') == '#' for neighbor in neighbors)
        new[cube] = next_state(state, active_neighbors)
        for cube in neighbors:
            new.setdefault(cube, '.')
    return new

cubes = {}
for y, row in enumerate(initial.splitlines()):
    for x, state in enumerate(row):
        #cube = (x, y, 0)
        cube = (x, y, 0, 0)
        cubes[cube] = state
        for cube in neighbors_coords(cube):
            cubes.setdefault(cube, '.')

for i in range(6):
    cubes = cycle(cubes)
print(sum(state == '#' for state in cubes.values()))
