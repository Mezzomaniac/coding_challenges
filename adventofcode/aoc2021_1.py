from downloader import download

download(2021, 1)
with open('aoc2021_1input.txt') as inputfile:
    depths = [int(n) for n in inputfile.readlines()]

count = 0
prev = depths[0]
for depth in depths[1:]:
    if depth > prev:
        count += 1
    prev = depth

print(count)

count = 0
prev = sum(depths[:3])
for i in range(4, len(depths)+1):
    value = sum(depths[i-3:i])
    if value > prev:
        count += 1
    prev = value

print(count)
