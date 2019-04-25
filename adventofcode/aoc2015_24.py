data = '''1
2
3
5
7
13
17
19
23
29
31
37
41
43
53
59
61
67
71
73
79
83
89
97
101
103
107
109
113'''

from functools import reduce
from operator import mul
from queue import Queue

PACKAGES = tuple(int(package) for package in data.split('\n')[::-1])
GOAL = sum(PACKAGES) // 4
#print(GOAL)

def qe(distribution):
    return reduce(mul, distribution)

combos = []
best_combo_length = len(PACKAGES)
frontier = Queue()
start = []#set()
frontier.put(start)
while not frontier.empty():
    current = frontier.get()
    #print(current)
    try:
        index = PACKAGES.index(current[-1]) + 1
    except IndexError:
        index = 0
    for package in PACKAGES[index:]:
        if package in current:
            continue
        next = current + [package]#| {package}
        weight = sum(next)
        length = len(next)
        if weight < GOAL and length <= best_combo_length:
        #if weight < GOAL:
            frontier.put(next)
        elif weight == GOAL and length <= best_combo_length:
            combos.append(next)
            best_combo_length = length
            #print(len(combos))

def divisible(packages):
    frontier = Queue()
    start = []#set()
    frontier.put(start)
    while not frontier.empty():
        current = frontier.get()
        #print(current)
        try:
            index = packages.index(current[-1]) + 1
        except IndexError:
            index = 0
        for package in packages[index:]:
            if package in current:
                continue
            next = current + [package]#| {package}
            weight = sum(next)
            if weight < GOAL:
                frontier.put(next)
            elif weight == GOAL:
                remaining = list(set(packages) - set(next))
                #print(next, remaining)
                if not remaining or divisible(remaining):
                    return True
    return False

combos.sort(key=qe)
combos.sort(key=len)
for combo in combos:
    print(combo)
    remaining = list(set(PACKAGES) - set(combo))
    if divisible(remaining):
        print(qe(combo))
        break
