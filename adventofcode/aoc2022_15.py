from downloader import download
from functools import lru_cache
import re

download(2022, 15)
with open('aoc2022_15input.txt') as inputfile:
    data = inputfile.read()

test = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''
#data = test
print(data)

sensors = {}
for line in data.splitlines():
    numbers = [int(n) for n in re.findall('[-\d]+', line)]
    sensors[complex(*(numbers[:2]))] = complex(*numbers[2:])

@lru_cache()
def distance(a, b):
    return int(abs((a - b).real) + abs((a - b).imag))

minx = int(min(sensor.real for sensor in sensors.keys()))
maxx = int(max(sensor.real for sensor in sensors.keys()))

covered = 0
for x in range(minx - 2000000, maxx + 2000001):
    if not x % 100000:
        print(x)
    point = x + 2000000j
    if point in sensors.values():
        continue
    for sensor, beacon in sensors.items():
        if distance(point, sensor) <= distance(sensor, beacon):
            #print(x, sensor)
            covered += 1
            break
print(covered)

limit = 4000000

found = False
for sensor, beacon in sensors.items():
    if found:
        break
    print(sensor)
    dist = distance(sensor, beacon) + 1
    minx = int(sensor.real) - dist
    maxx = int(sensor.real) + dist
    miny = int(sensor.imag) - dist
    midy = int(sensor.imag)
    maxy = int(sensor.imag) + dist
    x_range = list(range(minx, maxx + 1)) + list(range(minx + 1, maxx))
    y_range = list(range(midy, miny, -1)) + list(range(miny, maxy)) + list(range(maxy, midy, -1))
    outside = [complex(*(x, y)) for x, y in zip(x_range, y_range)]
    for point in outside:
        if not (0 <= point.real <= limit and 0 <= point.imag <= limit):
            continue
        for sensor2, beacon2 in sensors.items():
            if sensor2 == sensor:
                continue
            if distance(point, sensor2) <= distance(sensor2, beacon2):
                break
        else:
            found = True
            print(int(point.real * 4000000 + point.imag))
            break
