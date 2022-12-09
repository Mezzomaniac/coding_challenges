from downloader import download
from functools import reduce
from operator import mul
import numpy as np 

download(2022, 8)
with open('aoc2022_8input.txt') as inputfile:
    data = inputfile.read()

test = '''30373
25512
65332
33549
35390'''
#data = test

print(data)
forest = np.array([[int(char) for char in line] for line in data.splitlines()])

class  ViewingDistanceFactory:
    
    def __init__(self, tree):
        self.tree = tree
        self.blocked = False
        
    def viewing_distance(self, value, element):
        if self.blocked:
            return value
        if element >= self.tree:
            self.blocked = True
        return value + 1

visible = 0
highest_scenic_score = 0
it = np.nditer(forest, flags=['multi_index'])
while not it.finished:
    tree = it[0]
    left = forest[it.multi_index[0], :it.multi_index[1]]
    right = forest[it.multi_index[0], it.multi_index[1]+1:]
    up = forest[:it.multi_index[0], it.multi_index[1]]
    down = forest[it.multi_index[0]+1:, it.multi_index[1]]
    
    visible += any(np.all(tree > view) for view in (left, right, up, down))
    
    directions = (reversed(left), right, reversed(up), down)
    viewing_distances = (reduce(ViewingDistanceFactory(tree).viewing_distance, direction, 0) for direction in directions)
    scenic_score = reduce(mul, viewing_distances)
    highest_scenic_score = max(highest_scenic_score, scenic_score)
    
    it.iternext()

print(visible)
print(highest_scenic_score)
