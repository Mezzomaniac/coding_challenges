from functools import lru_cache

import numpy as np

SERIAL_NO = 9221

@lru_cache(maxsize=512)
def get_power_level1(cell):
    x, y = cell
    rack_id = x + 10
    power_level = (rack_id * y + SERIAL_NO) * rack_id
    return int(str(power_level).zfill(4)[-3]) - 5

maximum_square_power = -46
top_left = None
for x in range(1, 299):
    for y in range(1, 299):
        square = sum(get_power_level1((a, b)) for a in range(x, x+3) for b in range(y, y+3))
        if square > maximum_square_power:
            maximum_square_power = square
            top_left = (x, y)

#print(maximum_square_power)
print(*top_left, sep=',')


'''@lru_cache(maxsize=131072)
def get_power_level2(cell):
    x, y = cell
    rack_id = x + 10
    power_level = (rack_id * y + SERIAL_NO) * rack_id
    return int(str(power_level).zfill(4)[-3]) - 5

maximum_square_power = -450001
top_left = None
best_size = 0
for size in range(1, 301):
    print(size)
    for x in range(1, 302 - size):
        for y in range(1, 302 - size):
            square = sum(get_power_level2((a, b)) for a in range(x, x+size) for b in range(y, y+size))
            if square > maximum_square_power:
                maximum_square_power = square
                top_left = (x, y)
                best_size = size'''


def get_power_level3(index):
    y, x = index
    x += 1; y += 1
    rack_id = x + 10
    power_level = (rack_id * y + SERIAL_NO) * rack_id
    return int(str(power_level).zfill(4)[-3]) - 5

grid = np.zeros((300, 300))
it = np.nditer(grid, flags=['multi_index'], op_flags=['writeonly'])
while not it.finished:
    it[0] = get_power_level3(it.multi_index)
    it.iternext()
#print(grid)

stride = grid.strides[-1]
row_stride = stride * 300

sums = np.zeros((298, 298))
windows = np.lib.stride_tricks.as_strided(grid, (298, 298, 3, 3), strides=(row_stride, stride, row_stride, stride))
print(len(windows))
#print(windows)
np.sum(windows, axis=(2, 3), out=sums)
#print(sums)
#print(np.max(sums))
top_left = np.unravel_index(sums.argmax(), sums.shape)
top_left = (top_left[1]+1, top_left[0]+1)
print(*top_left, sep=',')


maximum_square_power = -450001
top_left = None
best_size = 0
for size in range(1, 301):
    print(size)
    sums = np.zeros((301 - size, 301 - size))
    windows = np.lib.stride_tricks.as_strided(grid, (301 - size, 301 - size, size, size), strides=(row_stride, stride, row_stride, stride))
    #print(windows)
    np.sum(windows, axis=(2, 3), out=sums)
    #print(sums)
    #print(np.max(sums))
    square = sums.max()
    if square > maximum_square_power:
        maximum_square_power = square
        top_left = np.unravel_index(sums.argmax(), sums.shape)
        top_left = (top_left[1]+1, top_left[0]+1)
        best_size = size
print(*top_left, best_size, sep=',')
