from downloader import download
from functools import lru_cache
import numpy as np

download(2021, 11)
with open('aoc2021_11input.txt') as inputfile:
    octopi = np.array([[int(n) for n in line] for line in inputfile.read().splitlines()])
print(octopi)

@lru_cache(maxsize=128)
def neighbors(y, x):
    coords = np.array([[y + a, x + b] for a in range(-1, 2) for b in range(-1, 2) if y + a in range(10) and x + b in range(10)]).T
    return (coords[0], coords[1])

flash_count = 0
step = 0
#for step in range(100):
while True:
    step += 1
    octopi += 1
    flashers = octopi > 9
    flashing = np.any(flashers)
    while flashing:
        octopi[flashers] = -10
        for coord in np.argwhere(flashers):
            octopi[neighbors(coord[0], coord[1])] += 1
        flashers = octopi > 9
        flashing = np.any(flashers)
    flashed = octopi < 0
    if np.all(flashed):
        print(step)
        break
    flash_count += np.count_nonzero(flashed)
    octopi[flashed] = 0
print(flash_count)
