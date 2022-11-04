from downloader import download
from functools import lru_cache
from itertools import product, combinations
from pprint import pprint
import re
import numpy as np

download(2021, 22)
with open('aoc2021_22input.txt') as inputfile:
    data = inputfile.read()
#print(data)

instruction_dict = {'off': 0, 'on': 1}

cubes = np.zeros((101, 101, 101))

def normalize1(string):
    values = string.split('=')[1]
    start, end = (int(value) for value in values.split('..'))
    start += 50
    start = min(max(start, 0), 101)
    end += 51
    end = max(min(end, 101), 0)
    return slice(start, end)

#cubes = np.zeros((200000, 200000, 200000))

@lru_cache(maxsize=None)
def normalize2(string, minimum, maximum):
    #print(string, minimum, maximum)
    values = string.split('=')[1]
    start, end = (int(value) for value in values.split('..'))
    start = min(max(start, minimum), maximum)
    end = max(min(end, maximum), minimum)
    #print(start, end)
    return range(start, end)

for step in data.splitlines():
    instruction, coords = step.split()
    slices = tuple(normalize1(coord) for coord in coords.split(','))
    #print(coords, slices)
    cubes[slices] = instruction_dict[instruction]
core = np.count_nonzero(cubes)
print(core)

extremes = {}
for axis in 'xyz':
    minimum = min(int(n) for n in re.findall(fr'{axis}=([\d-]+)', data))
    maximum = max(int(n) for n in re.findall(fr'{axis}=[\d-]+..([\d-]+)', data))
    extremes[axis] = (minimum, maximum)
#print(extremes)  #{'x': (-95851, 96459), 'y': (-95561, 99811), 'z': (-99062, 91425)}
extremes = {'x': (-96000, 98000), 'y': (-96000, 110000), 'z': (-100000, 93000)}

'''chunk_volume = 1000

total = 0
for x in range(*extremes['x'], chunk_volume):
    print(x)
    for y in range(*extremes['y'], chunk_volume):
        print(f'\t{y}')
        print(normalize2.cache_info())
        for z in range(*extremes['z'], chunk_volume):
            #print(normalize2.cache_info())
            #print(f'\t\t{z}')
            #print(x, y, z, total)
            cubes = set()
            for step in data.splitlines():
                #if (x, y, z) == (-96000, -36000, -40000):
                    #print(step)
                instruction, coords = step.split()
                ranges = (normalize2(coord, minimum, minimum + chunk_volume) for coord, minimum in zip(coords.split(','), (x, y, z)))
                if instruction == 'on':
                    cubes |= set(product(*ranges))
                else:
                    cubes -= set(product(*ranges))
                if cubes:
                    print(x, y, z, step, len(cubes), total)
            total += len(cubes)
print(total)'''

class Instruction:
    
    def __init__(self, index, step):
        self.index = index
        instruction, coords = step.split()
        self.instruction = instruction_dict[instruction]
        for coord in coords.split(','):
            axis, values = coord.split('=')
            start, end = (int(value) for value in values.split('..'))
            setattr(self, axis, (start, end + 1))
        self.overlaps = {self: self.volume()}
        self.counted = False
    
    def __eq__(self, other):
        return hash(self) == hash(other)
        
    def __hash__(self):
        return hash((self.index, self.instruction, self.x, self.y, self.z))

    def __repr__(self):
        return f'Instruction({self.index}, {self.instruction}, x={self.x}, y={self.y}, z={self.z})'
    
    def volume(self, other=None):
        if other is None:
            other = self
        x = max(min(self.x[1], other.x[1]) - max(self.x[0], other.x[0]), 0)
        y = max(min(self.y[1], other.y[1]) - max(self.y[0], other.y[0]), 0)
        z = max(min(self.z[1], other.z[1]) - max(self.z[0], other.z[0]), 0)
        return x * y * z

instructions = []
for index, step in enumerate(data.splitlines()):
    instruction = Instruction(index, step)
    instructions.append(instruction)
    '''if index < 20:
        continue
    for axis in (instruction.x, instruction.y, instruction.z):
        if not (all(value < -50 for value in axis) or all(value > 50 for value in axis)):
            print(instruction)'''

'''on_cubes = set()
for instruction in instructions:
    #print(instruction.volume())
    cubes = {(x, y, z) for x in range(*instruction.x) for y in range(*instruction.y) for z in range(*instruction.z)}
    if instruction.instruction:
        on_cubes |= cubes
    else:
        on_cubes -= cubes
    print(instruction.index, len(on_cubes))'''

#print(instructions)
#volumes = [instruction.volume() for instruction in instructions[20:]]
#print(volumes)
#print(len(volumes) - len(set(volumes)))
#volumes_and_instructions = [(instruction.volume(), str(instruction)) for instruction in instructions]
#for instruction in sorted(volumes_and_instructions):
    #print(instruction)

#def overlap(instruction1, instruction2):
    #return instruction1.volume(instruction2)
    #return all(
        #(getattr(instruction1, axis)[0] <= getattr(instruction2, axis)[0] < getattr(instruction1, axis)[1] 
        #or getattr(instruction2, axis)[0] <= getattr(instruction1, axis)[0] < getattr(instruction2, axis)[1]) 
        #for axis in 'xyz')'''

'''for instruction1, instruction2 in combinations(instructions, 2):
    overlap = instruction1.volume(instruction2)
    if overlap:
        instruction1.overlaps[instruction2] = overlap
        instruction2.overlaps[instruction1] = overlap'''
#for instruction in instructions:
    #pprint((instruction, sorted(instruction.index for instruction in instruction.overlaps)))


class Region:
    
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
    
    def __eq__(self, other):
        return hash(self) == hash(other)
        
    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return f'Region({self.name}, x={self.x}, y={self.y}, z={self.z})'
    
    def volume(self):
        return (self.x[1] - self.x[0]) * (self.y[1] - self.y[0]) * (self.z[1] - self.z[0])
    
def find_overlap(region, instruction):
    x_min = max(region.x[0], instruction.x[0])
    x_max = min(region.x[1], instruction.x[1])
    x = max(x_max - x_min, 0)
    y_min = max(region.y[0], instruction.y[0])
    y_max = min(region.y[1], instruction.y[1])
    y = max(y_max - y_min, 0)
    z_min = max(region.z[0], instruction.z[0])
    z_max = min(region.z[1], instruction.z[1])
    z = max(z_max - z_min, 0)
    if x and y and z:
        return Region(f'{region.name}&{instruction.index}', (x_min, x_max), (y_min, y_max), (z_min, z_max))

def compare_axes(region_axis, instruction_axis):
    order = sorted((*region_axis, *instruction_axis))
    if order == (region_axis[0], instruction_axis[0], instruction_axis[1], region_axis[1]):
        return 'in'
    if order == (instruction_axis[0], region_axis[0], region_axis[1], instruction_axis[1]):
        return 'out'
    if order == (region_axis[0], instruction_axis[0], region_axis[1], instruction_axis[1]) or order == (instruction_axis[0], region_axis[0], instruction_axis[1], region_axis[1]):
        return 'linked'

def split_region(region, overlap):
    new_regions = set()
    n = 1
    for x_min, x_max in zip(sorted([*region.x, *overlap.x])[:-1], sorted([*region.x, *overlap.x])[1:]):
        if x_min == x_max:
            continue
        for y_min, y_max in zip(sorted([*region.y, *overlap.y])[:-1], sorted([*region.y, *overlap.y])[1:]):
            if y_min == y_max:
                continue
            for z_min, z_max in zip(sorted([*region.z, *overlap.z])[:-1], sorted([*region.z, *overlap.z])[1:]):
                if z_min == z_max:
                    continue
                new_region = Region(f'{region.name}.{n}', (x_min, x_max), (y_min, y_max), (z_min, z_max))
                new_regions.add(new_region)
                n += 1
    new_regions.remove(overlap)
    return new_regions

regions = set()
for instruction in instructions:
    for region in regions.copy():
        overlap = find_overlap(region, instruction)
        if not overlap:
            continue
        overlapping_axes = {axis: compare_axes(getattr(region, axis), getattr(instruction, axis)) for axis in 'xyz'}
        if set(overlapping_axes.values()) == {'in'} and instruction.instruction:
            # instruction is both wholly inside a region and 'on'
            break
        regions.remove(region)
        if set(overlapping_axes.values()) == {'out'}:
            # region is wholly inside the instruction
            continue
        # in any other situation we split the region
        regions |= split_region(region, overlap)
    else:
        # if instruction is not both wholly inside a region and 'on'
        if instruction.instruction:
            regions.add(Region(str(instruction.index), instruction.x, instruction.y, instruction.z))
print(sum(region.volume() for region in regions))
