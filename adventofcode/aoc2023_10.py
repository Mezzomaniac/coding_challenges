from downloader import download

download(2023, 10)
with open('aoc2023_10input.txt') as inputfile:
    data = inputfile.read()

test_data1 = '''-L|F7
7S-7|
L|7||
-L-J|
L|-JF'''
test_data2 = '''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ'''
test_data3 = '''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''
test_data4 = '''..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........'''
test_data5 = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''
test_data6 = '''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L'''
#data = test_data6
print(data)

import queue

class Vector:
    
    def __init__(self, y, x):
        self.y = y
        self.x = x
    
    def __repr__(self):
        return f'Vector{(self.y, self.x)}'
    
    def __eq__(self, other):
        return (self.y, self.x) == (other.y, other.x)
    
    def __hash__(self):
        return hash((self.y, self.x))
    
    def __add__(self, other):
        return Vector(self.y + other.y, self.x + other.x)

    def __radd__(self, other):
        return Vector(other.y + self.y, other.x + self.x)

    def __mul__(self, other):
        return Vector(self.y * other, self.x * other)

    def __rmul__(self, other):
        return Vector(other * self.y, other * self.x)


grid = data.splitlines()
start_pos = Vector(*divmod(data.index('S'), len(grid[0]) + 1))
#print(start_pos)
height = len(grid)
width = len(grid[0])

pipes = {'|': ((-1, 0), (1, 0)), 
        '-': ((0, -1), (0, 1)),
        'L': ((-1, 0), (0, 1)),
        'J': ((-1, 0), (0, -1)),
        '7': ((0, -1), (1, 0)),
        'F': ((0, 1), (1, 0))}
for pipe, dirs in pipes.items():
    pipes[pipe] = [Vector(*dir) for dir in dirs]

DIRS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
DIRS = [Vector(*dir) for dir in DIRS]

def adjacents(pos):
    return (pos + dir for dir in DIRS[::2])
    
pos = None
path = [start_pos]
returned = False
while not returned:
    if pos is None:
        connection_found = False
        for adjacent in adjacents(start_pos):
            if connection_found:
                break
            if adjacent.y in (-1, height) or adjacent.x in (-1, width):
                continue
            pipe = grid[adjacent.y][adjacent.x]
            for connection in (adjacent + dir for dir in pipes.get(pipe, (Vector(0, 0), Vector(0, 0)))):
                if connection == start_pos:
                    path.append(adjacent)
                    pos = adjacent
                    connection_found = True
                    break
    #print(path, pos)
    pipe = grid[pos.y][pos.x]
    for connection in (pos + dir for dir in pipes.get(pipe, Vector(0, 0))):
        if len(path) >= 4 and connection == start_pos:
            returned = True
            break
        if connection not in path:
            path.append(connection)
            pos = connection
            break
print(len(path) // 2)


start = Vector(-.5, -.5)
visited = {start}
frontier = queue.Queue()
frontier.put(start)
while not frontier.empty():
    current_pos = frontier.get()
    for i, dir in list(enumerate(DIRS))[::2]:
        next_pos = current_pos + dir
        if next_pos in visited:
            continue
        if next_pos.y in (-1.5, height + .5) or next_pos.x in (-1.5, width + .5):
            # outside extended boundary
            continue
        if (first_diagonal := current_pos + .5 * DIRS[(i - 1) % len(DIRS)]) in path:
            path_index = path.index(first_diagonal)
            second_diagonal = current_pos + .5 * DIRS[(i + 1) % len(DIRS)]
            if second_diagonal in (path[(path_index - 1) % len(path)], path[(path_index + 1) % len(path)]):
                # blocked
                continue
        visited.add(next_pos)
        frontier.put(next_pos)
print(len(visited))
print((height + 1) * (width + 1) - len(visited - {vector + Vector(-.5, -.5) for vector in path}) - len(path))
