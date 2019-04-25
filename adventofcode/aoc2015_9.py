data = '''Faerun to Tristram = 65
Faerun to Tambi = 129
Faerun to Norrath = 144
Faerun to Snowdin = 71
Faerun to Straylight = 137
Faerun to AlphaCentauri = 3
Faerun to Arbre = 149
Tristram to Tambi = 63
Tristram to Norrath = 4
Tristram to Snowdin = 105
Tristram to Straylight = 125
Tristram to AlphaCentauri = 55
Tristram to Arbre = 14
Tambi to Norrath = 68
Tambi to Snowdin = 52
Tambi to Straylight = 65
Tambi to AlphaCentauri = 22
Tambi to Arbre = 143
Norrath to Snowdin = 8
Norrath to Straylight = 23
Norrath to AlphaCentauri = 136
Norrath to Arbre = 115
Snowdin to Straylight = 101
Snowdin to AlphaCentauri = 84
Snowdin to Arbre = 96
Straylight to AlphaCentauri = 107
Straylight to Arbre = 14
AlphaCentauri to Arbre = 46'''

from collections import defaultdict
from itertools import permutations

distances = defaultdict(dict)
for line in data.splitlines():
    city1, city2, dist = line.split()[::2]
    dist = int(dist)
    distances[city1][city2] = dist
    distances[city2][city1] = dist

min_path_length = 1000000
max_path_length = 0
for path in permutations(distances):
    path_length = sum(distances[city1][city2] for city1, city2 in zip(path, path[1:]))
    min_path_length = min(path_length, min_path_length)
    max_path_length = max(path_length, max_path_length)
print(min_path_length)
print(max_path_length)
