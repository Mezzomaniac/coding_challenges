data = '''114
51
122
26
121
90
20
113
8
138
57
44
135
76
134
15
21
119
52
118
107
99
73
72
106
41
129
83
19
66
132
56
32
79
27
115
112
58
102
64
50
2
39
3
77
85
103
140
28
133
78
34
13
61
25
35
89
40
7
24
33
96
108
71
11
128
92
111
55
80
91
31
70
101
14
18
12
4
84
125
120
100
65
86
93
67
139
1
47
38'''

from collections import defaultdict

adapters = [int(n) for n in data.splitlines()]
adapters.extend([0, max(adapters) + 3])
adapters.sort()
print(adapters)
differences = defaultdict(int)
cluster = [0]
combos = 1
redundancy = {1: 1, 2: 1, 3: 2, 4: 4, 5: 7}
for prev, current in zip(adapters, adapters[1:]):
    difference = current - prev
    differences[difference] += 1
    if difference == 3:
        combos *= redundancy[len(cluster)]
        cluster.clear()
    cluster.append(current)
#print(differences)
print(differences[1] * differences[3])
print(combos)
