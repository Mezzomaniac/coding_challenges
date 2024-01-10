from downloader import download

download(2023, 16)
with open('aoc2023_16input.txt') as inputfile:
    data = inputfile.read()
test_data = r'''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....'''
#data = test_data
data = data.replace('\\', '?')
print(data)

from collections import namedtuple
from queue import Queue

grid = data.splitlines()
height = len(grid)
width = len(grid[0])

Coord = namedtuple('Coord', 'y x')
Beam = namedtuple('Beam', 'pos dir')

def fire_beam(start_beam):
    energised_tiles = {start_beam.pos}
    visited_beams = {start_beam}
    frontier = Queue()
    frontier.put(start_beam)
    while not frontier.empty():
        current_beam = frontier.get()
        #print(current_beam)
        current_tile = grid[current_beam.pos.y][current_beam.pos.x]
        if current_tile == '/':
            next_dirs = [Coord(-current_beam.dir.x, -current_beam.dir.y)]
        elif current_tile == '?':#\\':
            next_dirs = [Coord(current_beam.dir.x, current_beam.dir.y)]
        elif current_tile == '-' and current_beam.dir.y:
            next_dirs = [Coord(0, -1), Coord(0, 1)]
        elif current_tile == '|' and current_beam.dir.x:
            next_dirs = [Coord(-1, 0), Coord(1, 0)]
        else:
            next_dirs = [current_beam.dir]
        for next_dir in next_dirs:
            next_pos = Coord(current_beam.pos.y + next_dir.y, current_beam.pos.x + next_dir.x)
            if not (0 <= next_pos.y < height and 0 <= next_pos.x < width):
                continue
            energised_tiles.add(next_pos)
            next_beam = Beam(next_pos, next_dir)
            next_tile = grid[next_beam.pos.y][next_beam.pos.x]
            if not (next_beam in visited_beams or (next_tile in '.-|' and Beam(next_pos, Coord(-next_dir.y, -next_dir.x)) in visited_beams)):
                frontier.put(next_beam)
                visited_beams.add(next_beam)
                #print(f'\t{next_beam}')
    return len(energised_tiles)

print(fire_beam(Beam(Coord(0, 0), Coord(0, 1))))


top_edges = (Coord(0, x) for x in range(width))
bottom_edges = (Coord(height -1, x) for x in range(width))
left_edges = (Coord(y, 0) for y in range(height))
right_edges = (Coord(y, width - 1) for y in range(height))
edges = [top_edges, bottom_edges, left_edges, right_edges]
dirs = [Coord(1, 0), Coord(-1, 0), Coord(0, 1), Coord(0, -1)]
print(max(fire_beam(Beam(pos, dir)) for edge, dir in zip(edges, dirs) for pos in edge))
