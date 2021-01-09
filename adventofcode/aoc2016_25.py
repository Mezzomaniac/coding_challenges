data = '''cpy a d
cpy 15 c
cpy 170 b
inc d
dec b
jnz b -2
dec c
jnz c -5
cpy d a
jnz 0 0
cpy a b
cpy 0 a
cpy 2 c
jnz b 2
jnz 1 6
dec b
dec c
jnz c -4
inc a
jnz 1 -7
cpy 2 b
jnz c 2
jnz 1 4
dec b
dec c
jnz 1 -4
jnz 0 0
out b
jnz a -19
jnz 1 -21'''

instructions = [line.split() for line in data.splitlines()]
toggle = {'dec': 'inc', 'tgl': 'inc', 'inc': 'dec', 'jnz': 'cpy', 'cpy': 'jnz', 'out': 'inc'}

def run(registers, goal=1000000):
    last_out = None
    transmission_length = 0
    index = 0
    while index < len(instructions):
        line = instructions[index]
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
        elif line[0] == 'tgl':
            other_index = index + registers[line[1]]
            try:
                instruction = instructions[other_index][0]
            except IndexError:
                index += 1
                continue
            instructions[other_index][0] = toggle[instruction]
        else:
            try:
                out = int(line[1])
            except ValueError:
                out = registers[line[1]]
            if not (out == 1 and last_out in (None, 0) or out == 0 and last_out in (None, 1)):
                return False
            if transmission_length >= goal:
                return True
            last_out = out
            transmission_length += 1
            if transmission_length and not transmission_length % 1000:
                print(transmission_length)
        index += 1

for a in range(180, 1000):
    registers = {letter: 0 for letter in 'abcd'}
    registers['a'] = a
    print(a, run(registers))
