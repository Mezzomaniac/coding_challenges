from downloader import download

download(2021, 2)
with open('aoc2021_2input.txt') as inputfile:
    instructions = inputfile.read().splitlines()
print(instructions)

horiz = 0
depth = 0
for instruction in instructions:
    direction, distance = instruction.split()
    distance = int(distance)
    if direction == 'forward':
        horiz += distance
    elif direction == 'down':
        depth += distance
    elif direction == 'up':
        depth -= distance
    else:
        raise ValueError
print(horiz * depth)

horiz = 0
depth = 0
aim = 0
for instruction in instructions:
    direction, distance = instruction.split()
    distance = int(distance)
    if direction == 'forward':
        horiz += distance
        depth += aim * distance
    elif direction == 'down':
        aim += distance
    elif direction == 'up':
        aim -= distance
    else:
        raise ValueError
print(horiz * depth)
