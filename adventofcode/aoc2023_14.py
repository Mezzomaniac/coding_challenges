from downloader import download

download(2023, 14)
with open('aoc2023_14input.txt') as inputfile:
    data = inputfile.read()
test_data = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''
#data = test_data
#print(data)

from collections import defaultdict
from operator import itemgetter

class RoundedRock:
    
    def __init__(self, y=0, x=0):
        self.y = y
        self.x = x
    
    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)
    
    def __eq__(self, other):
        return (self.y, self.x) == (other.y, other.x)
        
    def __getitem__(self, index):
        return (self.y, self.x)[index]
    
    def __hash__(self):
        return hash((self.y, self.x))
    
    def __repr__(self):
        return f'({self.y}, {self.x})'

cube_rocks = set()
round_rocks = set()
for y, row in enumerate(data.splitlines()):
    for x, space in enumerate(row):
        coords = RoundedRock(y, x)
        if space == '#':
            cube_rocks.add(coords)
        elif space == 'O':
            round_rocks.add(coords)

maxy = y
maxx = x

def tilt(round_rocks, axis=0, reverse=False, edge=0):
    moved_rocks = set()
    for rock in sorted(round_rocks, key=itemgetter(axis), reverse=reverse):
        rocks = cube_rocks | moved_rocks
        dir = (-1, 1)[reverse]
        if not axis:
            while rock.y != edge and RoundedRock(rock.y + dir, rock.x) not in rocks:
                rock.y += dir
        else:
            while rock.x != edge and RoundedRock(rock.y, rock.x + dir) not in rocks:
                rock.x += dir
        moved_rocks.add(rock)
    return moved_rocks

def total_load(round_rocks):
    return sum(maxy + 1 - rock.y for rock in round_rocks)

print(total_load(tilt(round_rocks)))

def cycle(round_rocks):
    for axis, reverse, edge in ((0, False, 0), (1, False, 0), (0, True, maxy), (1, True, maxx)):
        round_rocks = tilt(round_rocks, axis, reverse, edge)
    return round_rocks

cycles = 1000000000
history = defaultdict(list)
for i in range(cycles):
    round_rocks = cycle(round_rocks)
    load = total_load(round_rocks)
    #if load in history:
    print(i, load, history[load])
    history[load].append(i)

(cycles - 98) % (133 - 97)
