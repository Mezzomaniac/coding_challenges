from downloader import download

download(2017, 15)
with open('aoc2017_15input.txt') as inputfile:
    data = inputfile.read()
print(data)

matches = 0
a = 634
b = 301
for i in range(40_000_000):
    if not i % 1_000_000:
        print(i)
    a = a * 16807 % 2147483647
    b = b * 48271 % 2147483647
    matches += bin(a)[-16:] == bin(b)[-16:]
print(matches)

a_values = []
b_values = []
a = 634
b = 301
while min(len(a_values), len(b_values)) < 5_000_000:
    if not len(b_values) % 100_000:
        print(len(a_values), len(b_values))
    a = a * 16807 % 2147483647
    if not a % 4:
        a_values.append(a)
    b = b * 48271 % 2147483647
    if not b % 8:
        b_values.append(b)
matches = sum(bin(a)[-16:] == bin(b)[-16:] for a, b in zip(a_values, b_values))
print(matches)
