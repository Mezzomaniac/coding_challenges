from downloader import download

download(2022, 10)
with open('aoc2022_10input.txt') as inputfile:
    data = inputfile.read()
print(data)

test = '''addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop'''
#data = test

total_interesting_signal_strengths = 0
x = 1
cycle = 0
for op in data.splitlines():
    for i in range(1 + (op != 'noop')):
        cycle += 1
        if cycle % 40 and not cycle % 20:
            total_interesting_signal_strengths += cycle * x
    if op != 'noop':
        x += int(op.split()[1])
print(total_interesting_signal_strengths)

picture = ''
x = 1
cycle = 0
for op in data.splitlines():
    for i in range(1 + (op != 'noop')):
        picture += '.#'[cycle in range(x-1, x+2)]
        cycle += 1
        cycle %= 40
    if op != 'noop':
        x += int(op.split()[1])

for i, pixel in enumerate(picture):
    if not i % 40:
        print()
    print(pixel, end='')
