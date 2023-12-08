from downloader import download

download(2023, 8)
with open('aoc2023_8input.txt') as inputfile:
    data = inputfile.read()
#print(data)

from itertools import cycle
from math import lcm

instructions, node_data = data.split('\n\n')

instructions = cycle(instructions)

nodes = {}
for line in node_data.splitlines():
    node, exits = line.split(' = ')
    exits = exits[1:-1].split(', ')
    nodes[node] = exits

node = 'AAA'
steps = 0
while node != 'ZZZ':
    steps += 1
    node = nodes[node]['LR'.index(next(instructions))]
print(steps)


current_nodes = [node for node in nodes.keys() if node.endswith('A')]
steps = 0
periods = {}
while not all(node.endswith('Z') for node in current_nodes):
    if any(node.endswith('Z') for node in current_nodes):
        #print(steps, [node if node.endswith('Z') else '___' for node in current_nodes])
        [periods.setdefault(current_nodes.index(node), steps) for node in current_nodes if node.endswith('Z')]
        if len(periods) == len(current_nodes):
            #print(periods)
            break
    steps += 1
    direction = 'LR'.index(next(instructions))
    current_nodes = [nodes[node][direction] for node in current_nodes]
print(lcm(*periods.values()))
