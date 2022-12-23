from downloader import download
import re

download(2022, 22)
with open('aoc2022_22input.txt') as inputfile:
    data = inputfile.read()
test = '''        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5'''
#data = test
print(data)

map, instructions = data.split('\n\n')

width = max(len(line) for line in map.splitlines())
grid = []
for line in map.splitlines():
    grid.append(list(line.ljust(width)))
height = len(grid)

instructions = re.split('(R|L)', instructions.strip())

class Space:
    
    def __init__(self, y, x):
        self.y = y
        self.x = x
    
    def __repr__(self):
        return f'Space({self.y}, {self.x})'
    
    def __add__(self, other):
        return Space((self.y + other.y) % height, (self.x + other.x) % width)
    
    def __iter__(self):
        return iter((self.y, self.x))
        
directions = [Space(0, 1), Space(1, 0), Space(0, -1), Space(-1, 0)]

pos = Space(0, grid[0].index('.'))
dir = 0
for i, instruction in enumerate(instructions):
    #print(i, instruction, pos)
    if instruction.isdigit():
        for step in range(int(instruction)):
            new_pos = pos + directions[dir]
            y, x = new_pos
            while grid[y][x] == ' ':
                new_pos = new_pos + directions[dir]
                y, x = new_pos
            if grid[y][x] == '#':
                break
            pos = new_pos
    else:
        dir += (instruction == 'R') - (instruction == 'L')
        dir %= 4
y, x = pos
print((y + 1) * 1000 + (x + 1) * 4 + dir)

for index, row in enumerate(map.splitlines()):
    print(index, re.search('\S+', row.ljust(width)).span())

pos = Space(0, grid[0].index('.'))
dir = 0
for i, instruction in enumerate(instructions):
    print(i, instruction, pos, dir)
    if instruction.isdigit():
        for step in range(int(instruction)):
            new_pos = pos + directions[dir]
            new_dir = dir
            y, x = new_pos
            if grid[y][x] == ' ':
                y, x = pos
                if y == 0 and x < 100 and dir == 3:
                    new_pos = Space(x + 100, 0)
                    new_dir = 0
                elif y == 0 and dir == 3:
                    new_pos = Space(199, x - 100)
                    new_dir = 3
                elif x == 50 and y < 50:
                    new_pos = Space(149 - y, 0)
                    new_dir = 0
                elif x == 149 and dir == 0:
                    new_pos = Space(149 - y, 99)
                    new_dir = 2
                elif x >= 100:
                    new_pos = Space(x - 50, 99)
                    new_dir = 2
                elif x == 50 and dir == 2:
                    new_pos = Space(100, y - 50)
                    new_dir = 1
                elif y < 100:
                    new_pos = Space(49, y + 50)
                    new_dir = 3
                elif dir == 3:
                    new_pos = Space(x + 50, 50)
                    new_dir = 0
                elif x == 0 and y < 150:
                    new_pos = Space(149 - y, 50)
                    new_dir = 0
                elif x == 99 and dir == 0:
                    new_pos = Space(149 - y, 149)
                    new_dir = 2
                elif y == 149:
                    new_pos = Space(x + 100, 49)
                    new_dir = 2
                elif dir == 2:
                    new_pos = Space(0, y - 100)
                    new_dir = 1
                elif dir == 0:
                    new_pos = Space(149, y - 100)
                    new_dir = 3
                elif dir == 1:
                    new_pos = Space(0, x + 100)
                    new_dir = 1
                else:
                    raise ValueError
                y, x = new_pos
            if grid[y][x] == '#':
                break
            pos = new_pos
            dir = new_dir
    else:
        dir += (instruction == 'R') - (instruction == 'L')
        dir %= 4
y, x = pos
print((y + 1) * 1000 + (x + 1) * 4 + dir)
