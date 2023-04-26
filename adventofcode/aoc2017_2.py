from downloader import download

download(2017, 2)
with open('aoc2017_2input.txt') as inputfile:
    data = inputfile.read()
print(data)

checksum1 = 0
checksum2 = 0
for row in data.splitlines():
    numbers = {int(n) for n in row.split()}
    checksum1 += max(numbers) - min(numbers)
    if len(numbers) != len(row.split()):
        print('duplicated number')
    for a in numbers:
        for b in numbers:
            if a != b and not a % b:
                checksum2 += a // b
print(checksum1)
print(checksum2)
