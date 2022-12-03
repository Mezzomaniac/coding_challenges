from downloader import download
from string import ascii_letters

download(2022, 3)
with open('aoc2022_3input.txt') as inputfile:
    data = inputfile.read()
print(data)

total = 0
for line in data.splitlines():
    half = len(line) // 2
    total += ascii_letters.index((set(line[:half]) & set(line[half:])).pop()) + 1
print(total)

total = 0
bags = set()
for index, line in enumerate(data.splitlines(), 1):
    bags.add(frozenset(line))
    if not index % 3:
        total += ascii_letters.index(set(frozenset.intersection(*bags)).pop()) + 1
        bags.clear()
print(total)
