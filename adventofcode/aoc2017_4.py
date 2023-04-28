from downloader import download

download(2017, 4)
with open('aoc2017_4input.txt') as inputfile:
    data = inputfile.read()
print(data)

valid1 = 0
valid2 = 0
for line in data.splitlines():
    words = line.split()
    valid1 += len(words) == len(set(words))
    valid2 += len(words) == len(set(frozenset(word) for word in words))
print(valid1)
print(valid2)
