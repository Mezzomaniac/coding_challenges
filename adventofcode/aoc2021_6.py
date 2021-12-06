from downloader import download
from collections import Counter

download(2021, 6)
with open('aoc2021_6input.txt') as inputfile:
    fish = Counter([int(n) for n in inputfile.read().split(',')])
print(fish)

for day in range(256):
    fish = Counter({timer - 1: count for timer, count in fish.items()})
    fish[8] = fish[-1]
    fish[6] += fish[-1]
    del fish[-1]
print(sum(fish.values()))
