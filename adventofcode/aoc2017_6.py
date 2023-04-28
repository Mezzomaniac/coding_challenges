from downloader import download

download(2017, 6)
with open('aoc2017_6input.txt') as inputfile:
    data = inputfile.read()
print(data)

banks = [int(bank) for bank in data.split()]
seen = set()
cycles = 0
looped = False
while tuple(banks) not in seen:
    seen.add(tuple(banks))
    blocks = max(banks)
    index = banks.index(blocks)
    banks[index] = 0
    while blocks:
        index = (index + 1) % len(banks)
        banks[index] += 1
        blocks -= 1
    cycles += 1
    if tuple(banks) in seen and not looped:
        print(cycles)
        seen.clear()
        cycles = 0
        looped = True
print(cycles)
