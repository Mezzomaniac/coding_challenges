from downloader import download
import numpy as np

download(2017, 13)
with open('aoc2017_13input.txt') as inputfile:
    data = inputfile.read()

test = '''0: 3
1: 2
4: 4
6: 4'''
#data = test
print(data)

scanners = {}
severity = 0
for line in data.splitlines():
    depth, range_ = [int(n) for n in line.split(': ')]
    period = 2 * range_ - 2
    if not depth % period:
        severity += depth * range_
    scanners[depth] = period
print(severity)
print(scanners)

flags = np.ones(10000000, dtype=bool)
for depth, period in scanners.items():
    flags[(period - depth) % period::period] = False
    #print(np.flatnonzero(flags))
print(np.flatnonzero(flags).min())
