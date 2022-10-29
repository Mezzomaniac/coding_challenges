from downloader import download

download(2017, 2)
with open('aoc2017_2input.txt') as inputfile:
    data = inputfile.read()

checksum = 0
for row in data.splitlines():
    numbers = {int(n) for n in row.split()}
    checksum += max(numbers) - min(numbers)
print(checksum)
