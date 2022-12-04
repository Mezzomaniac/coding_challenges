from downloader import download

download(2022, 4)
with open('aoc2022_4input.txt') as inputfile:
    data = inputfile.read()
print(data)

total1 = 0
total2 = 0
for line in data.splitlines():
    first, second = [[int(n) for n in elf.split('-')] for elf in line.split(',')]
    total1 += first[0] <= second[0] <= second[1] <= first[1] or second[0] <= first[0] <= first[1] <= second[1]
    total2 += not (first[0] > second[1] or second[0] > first[1])
print(total1)
print(total2)
