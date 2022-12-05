from downloader import download
from more_itertools import chunked

download(2022, 5)
with open('aoc2022_5input.txt') as inputfile:
    data = inputfile.read()
print(data)

crates = [[] for crate in range(9)]
for line in data.splitlines()[:8]:
    for index, chunk in enumerate(chunked(line, 4)):
        chunk = ''.join(chunk).strip()
        if chunk:
            crates[index].append(chunk[1])
crates = [list(reversed(crate)) for crate in crates]
print(crates)

for instruction in data.splitlines()[10:]:
    instruction = instruction.split()
    from_crate = int(instruction[-3]) - 1
    quantity = int(instruction[1])
    #crates[int(instruction[-1]) - 1].extend(list(reversed(crates[from_crate][-quantity:])))
    crates[int(instruction[-1]) - 1].extend(crates[from_crate][-quantity:])
    crates[from_crate][-quantity:] = []

print(crates)
print(''.join(crate[-1] for crate in crates if crate))
