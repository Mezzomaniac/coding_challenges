passcode = 'bwnlcvfs'

from hashlib import md5
from queue import PriorityQueue

def point_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def open_doors(path):
    hash = md5(f'{passcode}{path}'.encode()).hexdigest()
    return {door for char, door in zip(hash, 'UDLR') if char in 'bcdef'}

DIRECTIONS = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

start = ''
locations = {'': (0, 0)}
goal = (3, 3)
frontier = PriorityQueue()
priority = distance(locations[start], goal)
priority = -priority
frontier.put((priority, start))
longest = 0
while not frontier.empty():
    current = frontier.get()[1]
    current_location = locations[current]
    if current_location == goal:
        #print(current)
        #break
        longest = max(longest, len(current))
        continue
    for direction in open_doors(current):
        next_location = point_add(current_location, DIRECTIONS[direction])
        if -1 in next_location or 4 in next_location:
            continue
        next = current + direction
        locations[next] = next_location
        priority = len(next) + distance(next_location, goal)
        priority = -priority
        frontier.put((priority, next))
print(longest)
