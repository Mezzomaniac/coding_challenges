from downloader import download
from collections import defaultdict
from queue import Queue

download(2021, 12)
with open('aoc2021_12input.txt') as inputfile:
    data = inputfile.read().splitlines()
print(data)

connections = defaultdict(set)
for line in data:
    first, second = line.split('-')
    connections[first].add(second)
    connections[second].add(first)
print(connections)

def second_small_allowed(path, next_cave):
    if next_cave in ('start', 'end'):
        return False
    smalls = [cave for cave in path if cave.islower()]
    return len(set(smalls)) == len(smalls)

paths = set()
frontier = Queue()
start = ('start',)
frontier.put(start)
while not frontier.empty():
    current = frontier.get()
    last = current[-1]
    if last == 'end':
        paths.add(current)
        continue
    for connection in connections[last]:
        if connection not in current or connection.isupper() or second_small_allowed(current, connection):
            frontier.put(current + (connection,))
print(len(paths))
