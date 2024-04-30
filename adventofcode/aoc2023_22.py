from downloader import download

download(2023, 22)
with open('aoc2023_22input.txt') as inputfile:
    data = inputfile.read()
test_data = '''1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''
#data = test_data
print(data)

from collections import defaultdict
from dataclasses import dataclass, astuple
import numpy as np

@dataclass
class Coord:
     x: int
     y: int
     z: int


class Brick:
    
    def __init__(self, id:int, pos1: Coord, pos2: Coord):
        self.id = id
        self.pos1 = pos1
        self.pos2 = pos2

    def __iter__(self):
        return iter((astuple(self.pos1), astuple(self.pos2)))
    
    def __repr__(self):
        return f'Brick{self.id, self.pos1, self.pos2}'
    
    def slice(self):
        return np.s_[self.pos1.z: self.pos2.z + 1, self.pos1.y: self.pos2.y + 1, self.pos1.x: self.pos2.x + 1]


def lower_slice(brick_slice):
    return (slice(brick_slice[0].start - 1, brick_slice[0].stop - 1, None), *brick_slice[1:])

# Create brick collection:
bricks = set()
maxx = 0
maxy = 0
maxz = 0
current_brick_id = 1
for line in data.splitlines():
    positions = line.split('~')
    brick = Brick(current_brick_id, *[Coord(*[int(n) for n in pos.split(',')]) for pos in positions])
    current_brick_id += 1
    maxx = max(maxx, brick.pos2.x)
    maxy = max(maxy, brick.pos2.y)
    maxz = max(maxz, brick.pos2.z)
    bricks.add(brick)
    # Check all bricks are 1x1x? and second given position is always greater than first:
    differences = sorted({pos2axis - pos1axis for pos1axis, pos2axis in zip(*brick)})
    if len(differences) == 3 or differences[0] != 0:
        print(brick)

# Catalog how the bricks support each other:
supported_by = defaultdict(set)
supports = defaultdict(set)
whole_space = np.ndarray((maxz + 1, maxy + 1, maxx + 1))
for brick in sorted(bricks, key=lambda brick: brick.pos1.z):
    brick_slice = brick.slice()
    while brick_slice[0].start > 1:
        lowered_slice = lower_slice(brick_slice)
        lowered_space = whole_space[lowered_slice]
        if not np.any(lowered_space):
            brick_slice = lowered_slice
        else:
            supporting_brick_ids = set(lowered_space.flatten())
            supporting_brick_ids.discard(0)
            supported_by[brick.id] |= supporting_brick_ids
            for supporting_brick_id in supporting_brick_ids:
                supports[supporting_brick_id].add(brick.id)
            break
    brick.pos1.z, brick.pos2.z = brick_slice[0].start, brick_slice[0].stop - 1
    whole_space[brick.slice()] = brick.id

# Part 1:
safe_to_disintegrate_total = 0
for brick_id in range(1, current_brick_id):
    for supported_brick_id in supports[brick_id]:
        if len(supported_by[supported_brick_id]) == 1:
            break
    else:
        safe_to_disintegrate_total += 1
print(safe_to_disintegrate_total)

# Part 2:
collapsing_total = 0
for brick_id in range(1, current_brick_id):
    removed_bricks_ids = {brick_id}
    still_removing_bricks = True
    while still_removing_bricks:
        still_removing_bricks = False
        for supported_brick_id in set.union(*(supports[removed_brick_id] for removed_brick_id in removed_bricks_ids)):
            if supported_brick_id not in removed_bricks_ids and supported_by[supported_brick_id] <= removed_bricks_ids:
                removed_bricks_ids.add(supported_brick_id)
                still_removing_bricks = True
    collapsing_total += len(removed_bricks_ids) - 1
print(collapsing_total)
