from downloader import download

download(2022, 6)
with open('aoc2022_6input.txt') as inputfile:
    data = inputfile.read()
print(data)

for i in range(4, len(data)):
    chunk = data[i-4:i]
    if len(set(chunk)) == 4:
        print(i)
        break

for i in range(14, len(data)):
    chunk = data[i-14:i]
    if len(set(chunk)) == 14:
        print(i)
        break
