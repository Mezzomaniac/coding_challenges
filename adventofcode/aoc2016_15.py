data = '''Disc #1 has 17 positions; at time=0, it is at position 5.
Disc #2 has 19 positions; at time=0, it is at position 8.
Disc #3 has 7 positions; at time=0, it is at position 1.
Disc #4 has 13 positions; at time=0, it is at position 7.
Disc #5 has 5 positions; at time=0, it is at position 1.
Disc #6 has 3 positions; at time=0, it is at position 0.'''

discs = {}
for pos, line in enumerate(data.splitlines(), 1):
    line = line.split()
    period = int(line[3])
    initial = int(line[-1][0])
    discs[period] = (period - pos - initial) % period
discs[11] = (11 - 7 - 0) % 11
discs = list(sorted(discs.items(), reverse=True))
print(discs)

factor, answer = discs[0]
for period, remainder in discs[1:]:
    while (answer % period) != remainder:
        answer += factor
    factor *= period
print(answer)
