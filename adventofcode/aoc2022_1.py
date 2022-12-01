from downloader import download

download(2022, 1)
with open('aoc2022_1input.txt') as inputfile:
    data = inputfile.read()
print(data)

elves = []
elf = 0
for line in data.splitlines():
    if not line:
        elves.append(elf)
        elf = 0
        continue
    elf += int(line)
print(elves)
print(max(elves))
print(sum(sorted(elves)[-3:]))
