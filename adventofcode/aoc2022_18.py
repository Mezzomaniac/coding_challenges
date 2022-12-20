from downloader import download
import sys

download(2022, 18)
with open('aoc2022_18input.txt') as inputfile:
    data = inputfile.read()
test1= '''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5'''
#data = test
#print(data)

cubes = {eval(line) for line in data.splitlines()}
#cubes = {(x, y, z) for x in range(4) for y in range(4) for z in range(4)}
#cubes -= {(x, y, z) for x in range(1, 3) for y in range(1, 3) for z in range(1, 3)}
#cubes.remove((0, 1, 1))
#print(cubes)

def adjacent_spaces(cube):
    x, y, z = cube
    return [(x-1, y, z), (x+1, y, z), (x, y-1, z), (x, y+1, z), (x, y, z-1), (x, y, z+1)]

surface_area = 0
for cube in cubes:
    for adjacent in adjacent_spaces(cube):
        if adjacent not in cubes:
            surface_area += 1
print(surface_area)

sys.setrecursionlimit(946)  # max allowed

def search_hole(space, hole, depth):
    #print(f'   {depth} {space} {len(hole)}')
    if space in cubes or space in hole:
        #print('   return')
        return hole
    hole.add(space)
    for adjacent in adjacent_spaces(space):
        hole |= search_hole(adjacent, hole, depth + 1)
    return hole

surface_area = 0
holes = set()
for cube in cubes:
    #print(cube)
    for adjacent in adjacent_spaces(cube):
        #print(f' {adjacent}')
        if adjacent in cubes or adjacent in holes:
            #print('  continue')
            continue
        try:
            holes |= search_hole(adjacent, set(), 0)
        except RecursionError:
            surface_area += 1
        #print(f'  {surface_area} {len(holes)}')
print(surface_area)

# < 4278  # using default recursion limit
