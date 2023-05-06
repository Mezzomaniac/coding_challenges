from downloader import download
from collections import defaultdict, deque

download(2017, 22)
with open('aoc2017_22input.txt') as inputfile:
    data = inputfile.read()
print(data)

test = '''..#
#..
...'''
#data = test

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
        
    def __hash__(self):
        return hash((self.x, self.y))
        
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f'Point({self.x}, {self.y})'

directions = deque([Point(0, -1), Point(-1, 0), Point(0, 1), Point(1, 0)])

infected = defaultdict(bool, [(Point(x, y), node == '#') for y, row in enumerate(data.splitlines()) for x, node in enumerate(row)])

pos = Point(len(data.splitlines()) // 2, len(data.splitlines()[0]) // 2)
infectious_bursts = 0
for burst in range(10000):
    status = infected[pos]
    directions.rotate((-1, 1)[status])
    infectious_bursts += not status
    infected[pos] = not status
    pos += directions[0]
    #print(pos, directions[0], [point for point, status in infected.items() if node])
    #print()
print(infectious_bursts)


directions = deque([Point(0, -1), Point(-1, 0), Point(0, 1), Point(1, 0)])

statuses = defaultdict(int, [(Point(x, y), (node == '#') * 2) for y, row in enumerate(data.splitlines()) for x, node in enumerate(row)])

pos = Point(len(data.splitlines()) // 2, len(data.splitlines()[0]) // 2)
infectious_bursts = 0
for burst in range(10000000):
    status = statuses[pos]
    directions.rotate((-1, 0, 1, 2)[status])
    infectious_bursts += status == 1
    statuses[pos] = (status + 1) % 4
    pos += directions[0]
    #print(pos, directions[0], statuses)
    #print()
print(infectious_bursts)
