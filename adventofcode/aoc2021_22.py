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

cubes = np.zeros((100, 100, 100))

def normalize1(string):
    values = string.split('=')[1]
    start, end = (int(value) for value in values.split('..'))
    start += 50
    start = min(max(start, 0), 100)
    end += 51
    end = max(min(end, 100), 0)
    return slice(start, end)

#cubes = np.zeros((200000, 200000, 200000))

@lru_cache(maxvolume=None)
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
#print(extremes)
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
    
    def __init__(self, order, step):
        self.order = order
        instruction, coords = step.split()
        self.instruction = instruction
        for coord in coords.split(','):
            axis, values = coord.split('=')
            start, end = (int(value) for value in values.split('..'))
            setattr(self, axis, (start, end + 1))
        self.overlaps = {self: self.volume()}
        self.counted = False
    
    def __eq__(self, other):
        return hash(self) == hash(other)
        
    def __hash__(self):
        return hash((self.order, self.instruction, self.x, self.y, self.z))

    def __repr__(self):
        return f'Instruction({self.order}, {self.instruction} x={self.x}, y={self.y}, z={self.z})'
    
    def volume(self, other=None):
        if other is None:
            other = self
        x = max(min(self.x[1], other.x[1]) - max(self.x[0], other.x[0]), 0)
        y = max(min(self.y[1], other.y[1]) - max(self.y[0], other.y[0]), 0)
        z = max(min(self.z[1], other.z[1]) - max(self.z[0], other.z[0]), 0)
        return x * y * z

instructions = [Instruction(i, step) for i, step in enumerate(data.splitlines())]
#print(instructions)
#volumes = [step.volume() for step in instructions]
#print(volumes)
#print(len(volumes) - len(set(volumes)))
#volumes_and_steps = [(step.volume(), str(step)) for step in instructions]
#for step in sorted(volumes_and_steps):
    #print(step)

#def overlap(instruction1, instruction2):
    #return instruction1.volume(instruction2)
    #return all(
        #(getattr(instruction1, axis)[0] <= getattr(instruction2, axis)[0] < getattr(instruction1, axis)[1] 
        #or getattr(instruction2, axis)[0] <= getattr(instruction1, axis)[0] < getattr(instruction2, axis)[1]) 
        #for axis in 'xyz')'''

for instruction1, instruction2 in combinations(instructions, 2):
    overlap = instruction1.volume(instruction2)
    if overlap:
        instruction1.overlaps[instruction2] = overlap
        instruction2.overlaps[instruction1] = overlap
#for instruction in instructions:
    #pprint((instruction, sorted(instruction.order for instruction in instruction.overlaps)))
big_groups = {frozenset(f'{overlapper.order}:{overlapper.instruction}' for overlapper in instruction.overlaps) for instruction in instructions[20:]}
print(len(instructions[20:]), len(big_groups))
pprint(sorted(big_groups, key=lambda x: len(x)))

total = core + instructions[334].volume()

for instruction in instructions[:20]:
    instruction.counted = True
instructions[334].counted = True

for instruction in instructions:
    if instruction.counted:
        continue
    if instruction.volume() in (overlap for other, overlap in instruction.overlaps.items() if other is not instruction) \
    and all(other.instruction == 'on' for other in instruction.overlaps):
        instruction.counted = True

print(sum(instruction.counted == False for instruction in instructions))
