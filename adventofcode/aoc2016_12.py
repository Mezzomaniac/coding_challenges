data = '''cpy 1 a
cpy 1 b
cpy 26 d
jnz c 2
jnz 1 5
cpy 7 c
inc d
dec c
jnz c -2
cpy a c
inc a
dec b
jnz b -2
cpy c b
dec d
jnz d -6
cpy 16 c
cpy 17 d
inc a
dec d
jnz d -2
dec c
jnz c -5'''

registers = {letter: 0 for letter in 'abcd'}
registers['c'] = 1
data = data.splitlines()
index = 0
while index < len(data):
    line = data[index].split()
    if line[0] == 'cpy':
        try:
            registers[line[2]] = registers[line[1]]
        except KeyError:
            registers[line[2]] = int(line[1])
    elif line[0] == 'inc':
        registers[line[1]] += 1
    elif line[0] == 'dec':
        registers[line[1]] -= 1
    else:
        try:
            query = registers[line[1]]
        except KeyError:
            query = int(line[1])
        if query:
            index += int(line[2])
            continue
    index += 1
print(registers['a'])
