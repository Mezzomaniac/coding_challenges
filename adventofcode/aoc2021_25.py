from downloader import download
from copy import deepcopy

download(2021, 25)
with open('aoc2021_25input.txt') as inputfile:
    data = inputfile.read()
test_data = '''v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>'''
#data = test_data
print(data)
print()

sea_cucumbers = [list(line) for line in data.splitlines()]

height = len(sea_cucumbers)
width = len(sea_cucumbers[0])

step = 0
moved = True
while moved:
    moved = False
    sea_cucumbers_copy = deepcopy(sea_cucumbers)
    for y, row in enumerate(sea_cucumbers_copy):
        for x, space in enumerate(row):
            if space == '>':
                next_x = (x + 1) % width
                if sea_cucumbers_copy[y][next_x] == '.':
                    moved = True
                    sea_cucumbers[y][next_x] = '>'
                    sea_cucumbers[y][x] = '.'
    sea_cucumbers_copy = deepcopy(sea_cucumbers)
    for y, row in enumerate(sea_cucumbers_copy):
        for x, space in enumerate(row):
            if space == 'v':
                next_y = (y + 1) % height
                if sea_cucumbers_copy[next_y][x] == '.':
                    moved = True
                    sea_cucumbers[next_y][x] = 'v'
                    sea_cucumbers[y][x] = '.'
    #for row in sea_cucumbers:
        #print(''.join(row))
    step += 1
    print(step)

