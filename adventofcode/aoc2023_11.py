from downloader import download

download(2023, 11)
with open('aoc2023_11input.txt') as inputfile:
    data = inputfile.read()
    
test_data = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''
#data = test_data
print(data)

from itertools import combinations

grid = data.splitlines()
galaxies = set()
empty_rows = set()
for y, row in enumerate(grid):
    if '#' not in row:
        empty_rows.add(y)
    for x, space in enumerate(row):
        if space == '#':
            galaxies.add((y, x))
cols = [[row[x] for row in grid] for x in range(len(grid[0]))]
empty_cols = {x for x, col in enumerate(cols) if '#' not in col}

expansion_factor = 1
expansion_factor = 999999

answer = 0
for a, b in combinations(galaxies, 2):
    #print(a, b)
    answer += abs(a[0] - b[0]) + abs(a[1] - b[1]) + \
        len(set.intersection(empty_rows, range(min(a[0], b[0]), max(a[0], b[0])))) * expansion_factor + \
        len(set.intersection(empty_cols, range(min(a[1], b[1]), max(a[1], b[1])))) * expansion_factor
    #print(answer)
print(answer)
