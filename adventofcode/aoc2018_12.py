data = '''initial state: .#####.##.#.##...#.#.###..#.#..#..#.....#..####.#.##.#######..#...##.#..#.#######...#.#.#..##..#.#.#

#..#. => .
##... => #
#.... => .
#...# => #
...#. => .
.#..# => #
#.#.# => .
..... => .
##.## => #
##.#. => #
###.. => #
#.##. => .
#.#.. => #
##..# => #
..#.# => #
..#.. => .
.##.. => .
...## => #
....# => .
#.### => #
#..## => #
..### => #
####. => #
.#.#. => #
.#### => .
###.# => #
##### => #
.#.## => .
.##.# => .
.###. => .
..##. => .
.#... => #'''

from functools import lru_cache
from time import time

import numpy as np

data = data.splitlines()

GENERATIONS1 = 20
GENERATIONS2 = 50000000000

INITIAL_STATE = data[0][15:]

RULES = dict(rule.split(' => ') for rule in data[2:])
STR_TO_INT = '.#'

#@lru_cache(maxsize=1024)
def generate(generations, initial_state):
    extra = generations * 2 + 2
    zeros = '.' * extra
    pots = zeros + initial_state + zeros
    #print(pots)
    BLANKS = ['.', '.']
    for gen in range(generations):
        #if not gen % 1000000:
            #print(gen)
        pots = ''.join(BLANKS + [RULES[pots[start: start+5]] for start in range(len(pots) - 4)] + BLANKS)
        #print(pots)
    pots = np.array([STR_TO_INT.index(pot) for pot in pots])
    plants = np.nonzero(pots)[0]
    plants = plants - extra
    return plants.sum()

#print(generate(GENERATIONS1, INITIAL_STATE))

#print(generate(GENERATIONS2, INITIAL_STATE))

ZEROS = '..'

@lru_cache(maxsize=1024)
def generate_next(pots):
    BLANKS = ['.', '.']
    pots = ZEROS + pots + ZEROS
    pots = ''.join(BLANKS + [RULES[pots[start: start+5]] for start in range(len(pots) - 4)] + BLANKS)
    return pots

def plant_locations(pots):
    pots = np.array([STR_TO_INT.index(pot) for pot in pots])
    return np.nonzero(pots)[0]

#@lru_cache(maxsize=1024)
def generate2(generations, pots):
    pots = ZEROS + pots + ZEROS
    #print(pots, '\n')
    extra = generations * 2 + 2
    for gen in range(generations):
        #if not gen % 1000:
            #print(gen)
        pots = generate_next(pots)
        #print(pots, '\n')
        plants = plant_locations(pots)
        plants = plants - extra
        #print(plants)
    return plants.sum()

#print(generate2(GENERATIONS2, INITIAL_STATE))

last = 0
for gen in range(10, 400, 10):
    print(gen)
    
    #start = time()
    #print(generate(gen, INITIAL_STATE))
    #print(time() - start)

    #start = time()
    result = generate2(gen, INITIAL_STATE)
    #print(time() - start)
    print(result, result - last)
    last = result
    
    print()

print(5873 + (GENERATIONS2 - 90) * 62)
