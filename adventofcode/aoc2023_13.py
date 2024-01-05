from downloader import download

download(2023, 13)
with open('aoc2023_13input.txt') as inputfile:
    data = inputfile.read()
    
test_data = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''
#data = test_data
print(data)

import numpy as np

patterns = [np.array([list(row) for row in pattern.splitlines()]) for pattern in data.split('\n\n')]

def printable_pattern(pattern_array):
    return '\n'.join(''.join(row) for row in pattern_array)

def get_slice_args(reflection_line, limit):
    start1 = 0
    end1 = reflection_line
    start2 = 2 * reflection_line - 1
    end2 = reflection_line - 1
    if reflection_line > limit / 2:
        start1 = reflection_line
        end1 = limit
        start2 = reflection_line - 1
        end2 = 2 * reflection_line - 1 - limit
    return start1, end1, start2, end2

summary = 0
unsmudged_summary = 0
for pattern in patterns:
    height, width = pattern.shape
    for reflection_line in range(1, height):
        start1, end1, start2, end2 = get_slice_args(reflection_line, height)
        #print(reflection_line, start1, end1, start2, end2)
        area1 = pattern[start1: end1]
        area2 = pattern[start2: end2: -1]
        #print(printable_pattern(area1), printable_pattern(area2), sep='\n\n')
        if np.all(area1 == area2):
            #print(True)
            summary += 100 * reflection_line
        elif np.sum(area1 != area2) == 1:
            unsmudged_summary += 100 * reflection_line
    for reflection_line in range(1, width):
        start1, end1, start2, end2 = get_slice_args(reflection_line, width)
        #print(reflection_line, start1, end1, start2, end2)
        area1 = pattern[:, start1: end1]
        area2 = pattern[:, start2: end2: -1]
        #print(printable_pattern(area1), printable_pattern(area2), sep='\n\n')
        if np.all(area1 == area2):
            #print(True)
            summary += reflection_line
        elif np.sum(area1 != area2) == 1:
            unsmudged_summary += reflection_line
print(summary)
print(unsmudged_summary)
