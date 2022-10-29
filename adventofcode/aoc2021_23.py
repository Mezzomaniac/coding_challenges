from downloader import download
from queue import PriorityQueue

download(2021, 23)
with open('aoc2021_23input.txt') as inputfile:
    data = inputfile.read()
print(data)

class Space:
    
    def __init__(self, occupant='', restriction=''):
        self.occupant = occupant
        self.restriction = restriction
        self.neighbors = []
    
    def __repr__(self):
        return f'Space({self.occupant}, {self.restriction})'



spaces = []
for i in range(11):
    hallway = Space()
    if i:
        prev = spaces[i-1]
        hallway.neighbors.append(prev)
        prev.neighbors.append(hallway)
    spaces.append(hallway)
for i, occupants, restriction in zip(range(2, 9, 2), ('BB', 'CC', 'AD', 'DA'), 'ABCD'):
    room1 = Space(occupants[0], restriction)
    room2 = Space(occupants[1], restriction)
    hallway = spaces[i]
    hallway.neighbors.append(room1)
    room1.neighbors.extend([hallway, room2])
    room2.neighbors.append(room1)
    spaces.extend([room1, room2])
#print(spaces)
    

frontier = PriorityQueue()
costs = {}
