from downloader import download

download(2017, 5)
with open('aoc2017_5input.txt') as inputfile:
    data = inputfile.read()
#print(data)

original_instructions = [int(n) for n in data.splitlines()]

instructions = original_instructions.copy()
index = 0
steps = 0
while 0 <= index < len(instructions):
    offset = instructions[index]
    instructions[index] += 1
    index += offset
    steps += 1
print(steps)

instructions = original_instructions.copy()
index = 0
steps = 0
while 0 <= index < len(instructions):
    offset = instructions[index]
    if offset >= 3:
        instructions[index] -= 1
    else:
        instructions[index] += 1
    index += offset
    steps += 1
print(steps)
