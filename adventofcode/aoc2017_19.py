from downloader import download

download(2017, 19)
with open('aoc2017_19input.txt') as inputfile:
    data = inputfile.read()

test = '''     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ '''
#data = test

class Point:
    
    def __init__(self, y, x):
        self.y = y
        self.x = x
    
    def __eq__(self, other):
        return (self.y, self.x) == (other.y, other.x)
    
    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)
    
    def __repr__(self):
        return f'Point({self.y}, {self.x})'

directions = (Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0))

current_space = '|'
current = Point(0, data.index(current_space))
grid = data.splitlines()
height = len(grid)
width = len(grid[0])
dir = Point(1, 0)
letters = []
steps = 0
while True:
    steps += 1
    next = current + dir
    next_space = grid[next.y][next.x]
    #print(next, next_space)
    region = grid[next.y - 1][next.x - 1: next.x + 2] + '\n' + grid[next.y][next.x - 1: next.x + 2] + '\n' + grid[next.y + 1][next.x - 1: next.x + 2]
    if next_space == ' ':
        break
    if next_space.isalpha():
        letters.append(next_space)
    elif next_space == '+':
        if region.count(' ') != 6 or set(region) != {'|', '-', '+', '\n', ' '}:
            print(region)
        for direction in directions:
            neighbor = next + direction
            if neighbor == current or neighbor.y not in range(height) or neighbor.x not in range(width):
                continue
            if grid[neighbor.y][neighbor.x] != ' ':
                dir = direction
                #print(dir)
                break
        else:
            break
    current = next
print(''.join(letters))
print(steps)
