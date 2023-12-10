from downloader import download

download(2023, 9)
with open('aoc2023_9input.txt') as inputfile:
    data = inputfile.read()
print(data)

test_data = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''
#data = test_data

from itertools import pairwise

#histories = [[int(n) for n in line.split()] for line in data.splitlines()]
histories = [[int(n) for n in line.split()][::-1] for line in data.splitlines()]

result = 0
max_depth = 0
for sequence in histories:
    levels = [sequence]
    differences = sequence.copy()
    while any(differences):
        differences = list(b - a for a, b in pairwise(differences))
        levels.append(differences.copy())
    #print(levels)
    max_depth = max(max_depth, len(levels))
    difference = levels.pop().pop()
    for level in reversed(levels):
        #print(difference)
        #print(level)
        levels[-1].append(levels[-1][-1] + difference)
        difference = level.pop()
        levels.pop()
        #print(levels)
    result += difference
    #print(result)
    #print()
print(result)
print(max_depth)
