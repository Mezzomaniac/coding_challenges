from downloader import download

download(2022, 9)
with open('aoc2022_9input.txt') as inputfile:
    data = inputfile.read()
print(data)

test = '''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2'''
#data = test

class Position:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __contains__(self, item):
        return item in (self.x, self.y)
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __abs__(self):
        return Position(abs(self.x), abs(self.y))
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    
    def __iter__(self):
        return iter((self.x, self.y))
    
    def __repr__(self):
        return f'Position({self.x}, {self.y})'

directions = {'U': Position(0, -1), 'D': Position(0, 1), 'L': Position(-1, 0), 'R': Position(1, 0)}

def calculate_move(axis):
    try:
        return axis // abs(axis)
    except ZeroDivisionError:
        return 0

length = 10

rope = [Position(0, 0)] * length
visited = {rope[-1]}
for line in data.splitlines():
    direction, distance = line.split()
    for step in range(int(distance)):
        rope[0] = rope[0] + directions[direction]
        for i, knot in enumerate(rope[1:], 1):
            difference = rope[i-1] - knot
            if 2 in abs(difference):
                move = Position(*(calculate_move(axis) for axis in difference))
                rope[i] = knot + move
        visited.add(rope[-1])
print(len(visited))
