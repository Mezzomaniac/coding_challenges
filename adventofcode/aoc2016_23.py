data = '''cpy a b
dec b
cpy a d
cpy 0 a
cpy b c
inc a
dec c
jnz c -2
dec d
jnz d -5
dec b
cpy b c
cpy c d
dec d
inc c
jnz d -2
tgl c
cpy -16 c
jnz 1 c
cpy 73 c
jnz 71 d
inc a
inc d
jnz d -2
inc c
jnz c -5'''

from math import factorial

registers = {letter: 0 for letter in 'abcd'}
registers['a'] = 12
registers = {'a': 132 * factorial(10), 'b': 1, 'c': 2, 'd': 0}
instructions = [line.split() for line in data.splitlines()]
toggle = {'dec': 'inc', 'tgl': 'inc', 'inc': 'dec', 'jnz': 'cpy', 'cpy': 'jnz'}
index = 0
index = 16
for i in range(16+4, len(instructions), 2):
    instructions[i][0] = toggle[instructions[i][0]]
while index < len(instructions):
    line = instructions[index]
    if index > 22:
        print(index, line, registers)
    if line[0] == 'cpy':
        register = line[2]
        if register not in registers:
            index += 1
            continue
        try:
            registers[line[2]] = registers[line[1]]
        except KeyError:
            registers[line[2]] = int(line[1])
    elif line[0] == 'inc':
        registers[line[1]] += 1
    elif line[0] == 'dec':
        registers[line[1]] -= 1
    elif line[0] == 'jnz':
        try:
            query = registers[line[1]]
        except KeyError:
            query = int(line[1])
        if query:
            try:
                index += int(line[2])
            except ValueError:
                index += registers[line[2]]
            continue
    else:
        other_index = index + registers[line[1]]
        try:
            instruction = instructions[other_index][0]
        except IndexError:
            index += 1
            continue
        instructions[other_index][0] = toggle[instruction]
    index += 1
print(registers['a'])
