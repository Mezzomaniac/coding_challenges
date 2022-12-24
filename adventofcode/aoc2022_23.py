from downloader import download
from collections import deque
from functools import lru_cache

download(2022, 23)
with open('aoc2022_23input.txt') as inputfile:
    data = inputfile.read()
test1 = '''.....
..##.
..#..
.....
..##.
.....'''
test2 = '''..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............'''
#data = test2
print(data)

elves = set()
for y, row in enumerate(data.splitlines()):
    for x, col in enumerate(row):
        if col == '#':
            elves.add((x, y))
print(sorted(elves))
elf_count = len(elves)

@lru_cache()
def adjacent_spaces(elf, differentials=tuple((dx, dy) for dx in range(-1, 2) for dy in range(-1, 2))):
    x, y = elf
    adjacent = {(x + dx, y + dy) for dx, dy in differentials}
    adjacent.discard(elf)
    return adjacent

directions = deque([((-1, -1), (0, -1), (1, -1)), ((-1, 1), (0, 1), (1, 1)), ((-1, -1), (-1, 0), (-1, 1)), ((1, -1), (1, 0), (1, 1))])

#for round in range(10):
round = 1
while True:
    proposed_moves = {}
    nonmoving = 0
    for elf in elves:
        if adjacent_spaces(elf).isdisjoint(elves):
            proposed_moves[elf] = elf
            nonmoving += 1
        else:
            for direction in directions:
                if adjacent_spaces(elf, direction).isdisjoint(elves):
                    proposed_moves[elf] = (elf[0] + direction[1][0], elf[1] + direction[1][1])
                    break
            else:
                proposed_moves[elf] = elf
                nonmoving += 1
    print(round, nonmoving / elf_count)
    #print(sorted(proposed_moves.items()))
    moves = list(proposed_moves.values())
    if set(moves) == elves:
        print(round)
        break
    elves = {move if moves.count(move) == 1 else elf for elf, move in proposed_moves.items()}
    directions.rotate(-1)
    #print(sorted(elves))
    #print()
    round += 1

xs = [elf[0] for elf in elves]
minx = min(xs)
maxx = max(xs)
ys = [elf[1] for elf in elves]
miny = min(ys)
maxy = max(ys)
print(abs((maxx + 1 - minx) * (maxy + 1 - miny)) - len(elves))
