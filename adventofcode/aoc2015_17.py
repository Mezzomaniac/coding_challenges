data = '''50
44
11
49
42
46
18
32
26
40
21
7
18
43
10
47
36
24
22
40'''

from itertools import combinations

GOAL = 150

containers = [int(n) for n in data.splitlines()]

right_combos = 0
for r in range(len(containers) + 1):
    for combo in combinations(containers, r):
        right_combos += sum(combo) == GOAL
    if right_combos:
        break
print(right_combos)
